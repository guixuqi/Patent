import base64
import re
import requests
import json


def baidu_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    ak = "zdp2U8K1fM0jzzn2Yj5DSFxf"
    sk = "AQi884iRLZo7QwWcBic8z0hXEvv5aeE4"
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(ak, sk)
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    resp = requests.post(host, headers=headers)
    str = resp.content.decode()
    dict = json.loads(str)
    access_token = dict["access_token"]
    # print(access_token)  # 24.b66ce3ebf46186c1bf7497fcef4d9a93.2592000.1574472966.282335-17602022  有效期30天
    return access_token


def discern_code(code_path):
    access_token = baidu_access_token()
    # access_token = "24.757e0351ceacc4edaa9580e9971c06a6.2592000.1575448457.282335-17602022"
    # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + access_token
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
    headers1 = {"Content-Type": "application/x-www-form-urlencoded"}
    # 二进制方式打开图文件
    f = open(code_path, 'rb')
    # 参数image：图像base64编码
    img = base64.b64encode(f.read())
    # # params = {"image": img}
    # # u = "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/login-showPic.shtml"
    # # params = {"url": u}
    params = {"image": img, "probability": "true"}
    resp1 = requests.post(url, headers=headers1, params=params)
    str1 = resp1.content.decode()
    dict1 = json.loads(str1)
    result = dict1["words_result"][0]["words"]
    # pro = dict1["words_result"][0]["probability"]
    # print(result)
    # print(pro)
    s1 = re.search(r"(\d+)\D+(\d+)", result).group(1)
    s2 = re.search(r"(\d+)\D+(\d+)", result).group(2)
    op = re.search(r"\d+(\D+)\d+", result).group(1)
    a1 = int(s1)
    a2 = int(s2)
    ops = {"+": (lambda x, y: x + y), "-": (lambda x, y: x - y)}
    code = ops[op](a1, a2)
    return code
