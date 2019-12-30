# coding:utf-8
import re
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import mimetypes, os
from Logs.log import log1
from libs.config import to_adds, base_dir


def annex(path):
    try:
        data = open(path, 'rb')
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            ctype = 'application/x-zip-compressed'
        maintype, subtype = ctype.split('/', 1)
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        encoders.encode_base64(file_msg)
        basename = os.path.basename(path)
        file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
        return file_msg
    except:
        log1.error('添加文件失败！')


def run(data):
    # 发件人地址
    from_addr = 'sys_eip@szhorn.com'
    # 邮箱密码
    password = 'Aa666666'
    # 收件人地址
    to_addr = to_adds()[0]
    # 抄送
    cc = to_adds()[1:]
    toaddrs = [to_addr] + cc
    # 邮箱服务器地址
    smtp_server = 'smtp.exmail.qq.com'

    # 设置邮件信息
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    msg = MIMEMultipart()
    msg.add_header('From', 'sys_dev <%s>' % from_addr)
    msg.add_header('To', to_addr)
    msg.add_header('Cc', ','.join(cc))

    # 邮件标题
    msg['Subject'] = Header('<{}>{}新专利信息'.format(today_str, data["PAVIEW"]), 'utf-8').encode()

    # 添加附件
    file = base_dir + "\\main\\downfile\\{}\\{}.zip".format(data["PAVIEW"], data["ID"])
    imageApart = MIMEApplication(open(file, 'rb').read())
    imageApart.add_header('Content-Disposition', 'attachment', filename="{}.zip".format(data["PN"]))
    msg.attach(imageApart)

    # 邮件正文
    mail = ""
    mail += "发明名称:\t{}\n".format(data["TIVIEW"])
    mail += "申请号:\t{}\n".format(data["APO"])
    mail += "申请日:\t{}\n".format(data["APD"])
    mail += "公开（公告）号:\t{}\n".format(data["PN"])
    mail += "公开（公告）日:\t{}\n".format(data["PD"])
    mail += "IPC分类号:\t{}\n".format(data["ICST"])
    mail += "申请（专利权）人:\t{}\n".format(data["PAVIEW"])
    mail += "发明人:\t{}\n".format(data["INVIEW"])
    mail += "申请人地址:\t{}\n".format(data["AA"])
    mail += "CPC分类号:\t{}\n".format(data["CPC"])
    if data["ABVIEW1"]:
        mail += "摘要:\n{}".format(data["ABVIEW1"] + data["ABVIEW2"])
    if data["WG_DESC1"]:
        mail += "外观设计简要说明:\n{}".format(data["WG_DESC1"] + data["WG_DESC2"])
    textApart = MIMEText(mail, 'plain', 'utf-8')
    msg.attach(textApart)
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, toaddrs, msg.as_string())
    server.quit()


if __name__ == '__main__':
    datas = {}
    datas["PAVIEW"] = "00"
    datas["ID"] = "11"
    datas["PN"] = "cd"
    run(datas)