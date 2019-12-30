import os
import re
import shutil
import sys
from time import sleep
from selenium import webdriver
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from Logs.log import log1
from libs import send_mail
from libs.config import save_address, username, password, w0, w1, w2, w3, w4, n0
from libs.feiyi import proxy_server
from libs.utils import get_proxy_port, open_txt, view_split
import pyautogui
import pyperclip
from retrying import retry
from libs.baidu_api import discern_code
from libs.db_sql import max_apd, insert_db, select_companys
from datetime import datetime


class PatentData:
    """
    1.设置代理
    2.登录--保存验证码图片
    3.调用百度API识别验证码
    4.登录
    5.输入公司名称检索
    6.进入专利详览
    7.提取信息
    8.点击下载
    9.翻页
    """
    def __init__(self):
        # 设置代理
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('disable-infobars')
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # prefs = {"download.default_directory": downfile_path}
        prefs = {"download.prompt_for_download": True}
        self.option.add_experimental_option("prefs", prefs)
        # self.option.add_argument('--proxy-server=http://{}:{}'.format(proxy_server, get_proxy_port()))
        self.option.add_argument('--no-sandbox')
        self.dr = webdriver.Chrome(chrome_options=self.option)
        self.dr.maximize_window()
        self.dr.set_page_load_timeout(w0)
        self.dr.set_script_timeout(w0)
        self.login_url = "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml"
        self.index_url = "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uiIndex.shtml"
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.page_txt = self.base_dir + "\\main\\pages.txt"
        self.pages = 0
        self.datas = 0
        self.down_file_name = ""
        self.m_apd = None
        self.dict = {}

    @retry(stop_max_attempt_number=5)
    def parse_url(self, url):  # 发送请求
        self.dr.get(url)

    def login(self):  # 解析数据
        # 关闭开发模式扩展程序弹框
        pyautogui.moveTo(x=1336, y=80, duration=w3, tween=pyautogui.linear)
        pyautogui.click()
        # 1.保存验证码图片
        code_path = self.base_dir + "\\code_pic\\login-showPic.jpg"
        m = 0
        boor = False
        for i in range(n0):
            y0 = 495
            y1 = 365
            y2 = 435
            y3 = 495
            y4 = 620
            n = 25
            if m != 0:
                y0 = y0 - n
                y1 = y1 - n
                y2 = y2 - n
                y3 = y3 - n
                y4 = y4 - n
            self.remove_down_file(code_path)  # 清除login-showPic.jpg
            pyautogui.moveTo(x=1150, y=y0, duration=w3, tween=pyautogui.linear)
            pyautogui.rightClick()
            sleep(w2)
            pyautogui.typewrite(['down', 'down', 'enter'])
            sleep(w2)
            pyperclip.copy(code_path)
            sleep(0.8)
            # 粘贴
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.press('enter')
            sleep(w2)
            m += 1
            # 2. 识别验证码
            try:
                code = discern_code(code_path)
            except:
                self.dr.refresh()
                sleep(w4)
                continue
            # 3. 登录
            pyautogui.moveTo(x=1000, y=y1, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            pyperclip.copy(username)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.moveTo(x=1000, y=y2, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            pyperclip.copy(password)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.moveTo(x=1000, y=y3, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            pyperclip.copy(code)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.moveTo(x=1076, y=y4, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            sleep(w1)
            # 判断登录是否成功
            # pyautogui.click(x=140, y=88, clicks=2, interval=0, button='left', duration=1, tween=pyautogui.linear)
            pyautogui.moveTo(x=140, y=88, duration=w3, tween=pyautogui.linear)
            pyautogui.doubleClick()
            sleep(w2)
            # pyautogui.hotkey('ctrlleft', 'c')
            pyautogui.rightClick()
            sleep(w2)
            pyautogui.typewrite(['down', 'enter'])
            open_txt()
            with open(self.page_txt, "r+", errors="ignore") as f:
                login_name = f.read()
            with open(self.page_txt, "w", errors="ignore") as f:
                # if login_name == username:
                if re.search(username, login_name):
                    log1.info("登录OK")
                    boor = True
                    f.truncate()
                    break
                else:
                    self.dr.refresh()
                    sleep(w4)
                    f.truncate()
        return boor

    def enter_index(self, company):
        boor = False
        for i in range(n0):
            pyautogui.moveTo(x=670, y=560, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            pyperclip.copy(company)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.moveTo(x=1088, y=555, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            sleep(20)
            # 判断是否进入列表页
            pyautogui.hotkey('ctrlleft', 'a')
            sleep(w2)
            pyautogui.hotkey('ctrlleft', 'c')
            sleep(w2)
            open_txt()
            with open(self.page_txt, "r+", errors="ignore") as fr:
                index_page = fr.read()
            with open(self.page_txt, "w", errors="ignore") as fw:
                list_page = re.search(r"共(.*)页(.*)条数据", index_page)
                if list_page:
                    self.pages = list_page.group(1).strip()
                    self.datas = list_page.group(2).strip()
                    log1.info("{}列表页OK,共 {} 页 {} 条数据".format(company, self.pages, self.datas))
                    if not (int(self.pages) > 0 and int(self.datas) > 0):
                        self.dr.refresh()
                        sleep(w4)
                    else:
                        boor = True
                    fw.truncate()
                    break
                else:
                    fw.truncate()
                    self.dr.refresh()
                    sleep(w4)
        if not boor:
            log1.info("{}进入列表页失败".format(company))
        return boor

    def enter_detail(self, company):
        downfile_path = self.base_dir + "\\main\\downfile\\{}\\".format(company)
        try:
            os.makedirs(downfile_path)
            new_company = True
        except:
            new_company = False
        # 1.点击检索历史--列表式
        pyautogui.moveTo(x=300, y=392, duration=w3, tween=pyautogui.linear)
        pyautogui.click()
        pyautogui.moveTo(x=515, y=465, duration=w3, tween=pyautogui.linear)
        pyautogui.click()
        sleep(w4)
        download_num = 0
        for p in range(1, int(self.pages)+1):
            y0 = 583
            y1 = 207
            num = 0
            per = 12
            if p == int(self.pages):
                per = int(self.datas) - (int(self.pages)-1) * 12
            for i in range(per):
                if i == 5:
                    # 2.滑动滚动条至底部指定位置
                    pyautogui.moveTo(x=1430, y=782, duration=w3, tween=pyautogui.linear)
                    pyautogui.click()
                    sleep(w2)
                    pyautogui.moveTo(x=1150, y=y1, duration=w3, tween=pyautogui.linear)
                    pyautogui.click()
                    y1 += 55
                elif i < 5:
                    # 3.点击详览, re提取dr.page_source数据
                    pyautogui.moveTo(x=1150, y=y0, duration=w3, tween=pyautogui.linear)
                    pyautogui.click()
                    y0 += 55
                else:
                    pyautogui.moveTo(x=1150, y=y1, duration=w3, tween=pyautogui.linear)
                    pyautogui.click()
                    y1 += 55
                sleep(20)
                handles = self.dr.window_handles
                try:
                    self.dr.switch_to.window(handles[1])
                except:
                    continue
                # 判断是否进入详情页--提取数据
                self.dict = {}
                self.down_file_name = ""
                if self.parse_data(company):
                    self.dr.close()
                    self.dr.switch_to.window(handles[0])
                    if num == 1:
                        return
                    num += 1
                    continue
                download_num += 1
                log1.info("{}共更新了{}条".format(company, download_num))
                # 4.点击下载--点击保存验证码--输入验证码--点击下载--输入保存地址保存
                if not self.down_file_name:
                    continue
                if not new_company:
                    self.download(company, downfile_path)  # 下载(新公司不下载)
                # 5.关闭当前详情页
                self.dr.close()
                self.dr.switch_to.window(handles[0])
                # 6.循环3-4-5
            # 7.定位"共 页"前的输入框--输入页码--enter
            if p < int(self.pages):
                # 8.循环2-3-4-5-6-7
                pyautogui.moveTo(x=1115, y=100, duration=w3, tween=pyautogui.linear)
                pyautogui.doubleClick()
                sleep(w2)
                pyperclip.copy(p+1)
                sleep(0.8)
                # 粘贴
                pyautogui.hotkey('ctrlleft', 'V')
                sleep(w2)
                pyautogui.press('enter')
                sleep(w4)
                # 2.滑动滚动条至最顶部
                pyautogui.moveTo(x=1405, y=763, duration=w3, tween=pyautogui.linear)
                pyautogui.click()
                sleep(w2)

    def download(self, company, downfile_path):
        down_file_path = downfile_path + "{}.zip".format(self.down_file_name)
        for ii in range(n0):
            y = 463 + (len(self.dict["TIVIEW"])//15)*20
            pyautogui.moveTo(x=156, y=y, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            sleep(w4)
            code_path = self.base_dir + "\\code_pic\\download-showPic.jpg"
            self.remove_down_file(code_path)
            pyautogui.moveTo(x=650, y=517, duration=w3, tween=pyautogui.linear)
            pyautogui.rightClick()
            sleep(w2)
            pyautogui.typewrite(['down', 'down', 'enter'])
            sleep(w2)
            # 将地址以及文件名复制
            pyperclip.copy(code_path)
            sleep(0.8)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.press('enter')
            sleep(w2)
            try:
                code = discern_code(code_path)
            except:
                pyautogui.moveTo(x=914, y=570, duration=w3, tween=pyautogui.linear)
                pyautogui.click()
                continue
            if not code:
                break
            # code = input("code:")
            pyautogui.moveTo(x=572, y=517, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            pyperclip.copy(code)
            sleep(0.8)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.moveTo(x=972, y=570, duration=w3, tween=pyautogui.linear)
            pyautogui.click()
            sleep(w4)
            pyperclip.copy(down_file_path)
            sleep(0.8)
            pyautogui.hotkey('ctrlleft', 'V')
            pyautogui.press('enter')
            sleep(w1)
            # 判断下载是否成功
            if not os.path.exists(down_file_path):
                sleep(w1)
                pyautogui.moveTo(x=914, y=570, duration=w3, tween=pyautogui.linear)
                pyautogui.click()
                self.dr.refresh()
                sleep(2)
                continue
            else:
                break
        if not os.path.exists(down_file_path):
            log1.info("{}下载失败".format(self.down_file_name))
        else:
            try:
                send_mail.run(self.dict)  # 发送邮件
                log1.info("邮件发送OK")
            except Exception as e:
                log1.error("{}{}邮件发送失败:{}".format(company, self.dict["ID"], e))

    def parse_data(self, company):
        pyautogui.hotkey('ctrlleft', 'a')
        sleep(w2)
        pyautogui.hotkey('ctrlleft', 'c')
        sleep(w2)
        open_txt()
        dict = {}
        with open(self.page_txt, "r+", errors="ignore") as fr:
            detail_page = fr.read().replace('\n', '').replace('\r', '').replace('\t', '').strip()
            TIVIEW = re.search("发明名称 ---  (.*)申请号", detail_page)
            APO = re.search("申请号­(.*)申请日", detail_page)
            if not APO:
                APO = re.search("申请号-(.*)申请日", detail_page)
            APD = re.search("申请日(.*)公开（公告）号", detail_page)
            PN = re.search("公开（公告）号­(.*)公开（公告）日", detail_page)
            if not PN:
                PN = re.search("公开（公告）号-(.*)公开（公告）日", detail_page)
            PD = re.search("公开（公告）日(.*)IPC分类号", detail_page)
            if not PD:
                PD = re.search("公开（公告）日(.*)外观设计洛迦诺分类号", detail_page)
            ICST = re.search("IPC分类号(.*)申请（专利权）人", detail_page)
            if not ICST:
                ICST = re.search("外观设计洛迦诺分类号(.*)申请（专利权）人", detail_page)
            PAVIEW = re.search("申请（专利权）人(.*)发明人", detail_page)
            if not PAVIEW:
                PAVIEW = re.search("申请（专利权）人(.*)设计人", detail_page)
            INVIEW = re.search("发明人(.*)优先权号", detail_page)
            if not INVIEW:
                INVIEW = re.search("设计人(.*)优先权号", detail_page)
            PR = re.search("优先权号(.*)优先权日", detail_page)
            PRD = re.search("优先权日(.*)申请人地址", detail_page)
            AA = re.search("申请人地址(.*)申请人邮编", detail_page)
            AZ = re.search("申请人邮编(.*)CPC分类号", detail_page)
            CPC = re.search("CPC分类号(.*)摘要翻译", detail_page)
            if not CPC:
                CPC = re.search("CPC分类号(.*)外观设计简要说明翻译", detail_page)
            ABVIEW = re.search("摘要翻译(.*)摘要附图", detail_page)
            ABVIEW = ABVIEW.group(1) if ABVIEW else ""
            WG_DESC = re.search("外观设计简要说明翻译(.*)外观设计图", detail_page)
            WG_DESC = WG_DESC.group(1) if WG_DESC else ""
            dict["TIVIEW"] = TIVIEW.group(1) if TIVIEW else ""
            dict["APO"] = APO.group(1) if APO else ""
            dict["APD"] = APD.group(1) if APD else ""
            dict["PN"] = PN.group(1) if PN else ""
            dict["PD"] = PD.group(1) if PD else ""
            dict["ICST"] = ICST.group(1) if ICST else ""
            dict["PAVIEW"] = PAVIEW.group(1).replace(";", "") if PAVIEW else company
            dict["INVIEW"] = INVIEW.group(1) if INVIEW else ""
            dict["PR"] = PR.group(1) if PR else ""
            dict["PRD"] = PRD.group(1) if PRD else ""
            dict["AA"] = AA.group(1) if AA else ""
            dict["AZ"] = AZ.group(1) if AZ else ""
            dict["CPC"] = CPC.group(1) if CPC else ""
            dict["ABVIEW1"], dict["ABVIEW2"] = view_split(ABVIEW)
            dict["WG_DESC1"], dict["WG_DESC2"] = view_split(WG_DESC)
            dict["ID"] = dict["APO"] + dict["PN"]
        with open(self.page_txt, "w", errors="ignore") as fw:
            fw.truncate()
        self.down_file_name = dict["ID"]
        self.dict = dict
        if self.save_data(dict):
            return True

    def save_data(self, dict):  # 保存数据
        try:
            apd = dict["APD"]
            APD_Date = datetime.strptime(apd, "%Y.%m.%d")
            if self.m_apd and (self.m_apd - APD_Date).days >= 0:
                return True
            insert_db(dict)
        except Exception as e:
            log1.error(e)
            return True

    def remove_down_file(self, down_path):
        if os.path.exists(down_path):
            os.remove(down_path)

    def move_down_file(self, down_path):
        new_path = self.base_dir + "\\code_pic\\login-showPic.jpg"
        self.remove_down_file(new_path)
        shutil.move(down_path, new_path)
        return new_path

    def get_companys(self):
        results = select_companys()
        comps = []
        for result in results:
            if result[0]:
                comp = result[0].replace(" ;", "").replace("(", "（").replace(")", "）").replace(" ", "").strip()
                comps.append(comp)
        return comps

    def run(self):
        self.parse_url(self.login_url)
        sleep(w1)
        if not self.login():
            log1.info("登录失败")
            self.dr.quit()
            return
        companys = self.get_companys()
        # companys = ["中山奥凯华泰电子有限公司"]
        for company in companys:
            self.m_apd = max_apd(company)
            if not self.enter_index(company):
                continue
            self.enter_detail(company)
            self.dr.refresh()
            sleep(w4)
        self.dr.quit()


if __name__ == '__main__':
    pd = PatentData()
    pd.run()
