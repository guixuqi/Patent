# -*- coding: UTF-8 –*-
import requests
import sys
import time
import hashlib
import logging
import json

proxy_username = 'guixuqitp1'
proxy_passwd = '92768899'
proxy_server = '183.129.244.16'
proxy_port = '88'
pattern = 'json'  # API访问返回信息格式：json和text可选
num = 1  # 获取代理端口数量

key_name = 'user_name='
key_timestamp = 'timestamp='
key_md5 = 'md5='
key_pattern = 'pattern='
key_num = 'number='
key_port = 'port='


# 返回当前时间戳（单位为 ms）
def get_timestamp():
    timestamp = round(time.time() * 1000)
    return timestamp


# 进行md5加密
def get_md5_str(s):
    return hashlib.md5(bytes(s.encode('utf-8'))).hexdigest()


# 返回请求分配代理端口URL链接
def get_open_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/open?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) + \
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern + \
           '&' + key_num + str(num)


# 返回释放代理端口URL链接
def get_close_url(auth_port):
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/close?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) + \
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern + \
           '&' + key_port + auth_port


# 返回重置本用户已使用ip URL链接
def get_reset_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + proxy_port + '/reset_ip?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) + \
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern


# 使用代理进行测试 url为使用代理访问的链接，auth_port为代理端口
def testing(url, auth_port):
    proxies = {'http': "http://" + proxy_server + ':' + auth_port,
               'https': 'http://' + proxy_server + ':' + auth_port, }
    try:
        s = requests.Session()
        s.proxies.update(proxies)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        ret = s.get(url, headers=header)
        msg = str(ret.status_code)
    except requests.exceptions.SSLError as e:
        msg = repr(e)
    except Exception as e:
        msg = repr(e)
    return msg


# 实例简单演示如何正确获取代理端口，使用代理服务测试访问https://ip.cn，验证后释放代理端口
if __name__ == '__main__':
    logging.basicConfig(filename='./proxy.log', level=logging.INFO)
    count = 0
    port = ''
    # 测试访问链接
    # test_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/login-showPic.shtml'
    test_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml'
    # while True:
    while count < 1:
        try:
            open_url = get_open_url()
            r = requests.get(open_url, timeout=5)
            result = str(r.content.decode())
            logging.info('open_url||' + result)
            json_obj = json.loads(result)
            code = json_obj['code']
            if json_obj['code'] == 108:
                reset_url = get_reset_url()
                r = requests.get(reset_url, timeout=5)
            elif json_obj['code'] == 100:
                port = str(json_obj['port'][0])
        except Exception as e:
            logging.info('open_url||' + repr(e))
            continue
        tmp = testing(test_url, port)
        logging.info('使用代理测试访问返回状态码||' + tmp)
        try:
            close_url = get_close_url(port)
            r = requests.get(close_url, timeout=5)
            result = str(r.content)
            logging.info('close_url||' + result)
        except Exception as e:
            logging.info('close_url||' + repr(e))
            continue
        count += 1
