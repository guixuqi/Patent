import json
import random
import pyautogui
import requests
from Logs.log import log1
from libs.feiyi import get_open_url, get_reset_url, get_close_url, proxy_server
from selenium import webdriver
import time
from selenium.webdriver import ChromeOptions

# 随机UA
def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


# 获取飞蚁代理IP
def get_proxy_port():
    port = ""
    for i in range(3):
        try:
            open_url = get_open_url()
            r = requests.get(open_url, timeout=5)
            result = str(r.content.decode())
            json_obj = json.loads(result)
            code = json_obj['code']
            if code == 108:
                reset_url = get_reset_url()
                requests.get(reset_url, timeout=5)
            elif code == 100:
                port = str(json_obj['port'][0])
                break
        except Exception as e:
            log1.error(e)
            continue
    return port


# 回收代理IP
def close_proxy_port(port):
    for i in range(3):
        try:
            close_url = get_close_url(port)
            requests.get(close_url, timeout=5)
            break
        except Exception as e:
            continue


def get_proxy_ip(port):
    if not port:
        log1.info("无法获取到代理IP端口")
        return "", ""
    proxies = {'http': "http://" + proxy_server + ':' + port,
               'https': 'http://' + proxy_server + ':' + port}
    return proxies


def view_split(ABVIEW):
    ABVIEW = ABVIEW.encode('gbk', 'ignore')
    length = len(ABVIEW)
    num = 4000
    if length < num:
        ABVIEW1 = ABVIEW
        ABVIEW2 = b""
    else:
        ABVIEW1 = ABVIEW[0:num]
        ABVIEW2 = ABVIEW[num:num * 2]
    return ABVIEW1.decode('gbk'), ABVIEW2.decode('gbk')


def getResponseHeader(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'request']
            if response[u'url'] == browser.current_url:
                return response[u'headers']
        except:
            pass
    return None


def getWebdriverHeader(browser):
    for i in browser.get_log('performance'):
        dic_info = json.loads(i["message"])  # 把json格式转成字典。
        info = dic_info["message"]['params']  # request 信息，在字典的 键 ["message"]['params'] 中。
        if 'request' in info:  # 如果找到了 request 信息，就终断循环。
            # print(info['request']["headers"])
            return info['request']["headers"]


def get_cookie(url):
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    # 启动selenium获取浏览器cookies
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--no-sandbox')
    # option.set_headless()
    dr = webdriver.Chrome(options=option)
    dr.get(url)
    headers = getWebdriverHeader(dr)
    cookie = dr.get_cookies()
    time.sleep(1)
    # dr.quit()
    cookie_jar = requests.cookies.RequestsCookieJar()
    for i in cookie:  # 添加cookie到CookieJar
        cookie_jar.set(i["name"], i["value"])
    return cookie_jar, headers


def open_txt():
    pyautogui.hotkey('ctrlleft', 'shift', 'q')
    time.sleep(5)
    pyautogui.hotkey('ctrlleft', 'V')
    time.sleep(1)
    pyautogui.hotkey('ctrlleft', 's')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
    pyautogui.press('enter')

