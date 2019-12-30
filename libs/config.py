import cx_Oracle
import os

# dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")  # 数据库配置
conn = cx_Oracle.connect("EIP", "EIP", dsnStr, threaded=True)
c = conn.cursor()

# username = "0A2831"  # 国知局网站账号与密码
# password = "guixuqi7310"
# username = "guixuqi2019"  # 国知局网站账号与密码
# password = "guixuqi7310"
username = "初七下八aa96"  # 国知局网站账号与密码
password = "fighting1996"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_address = base_dir + "\\code_pic\\"

# 等待时间
w0 = 120   # 加载网页最大
w1 = 20    # 跳转新页面
w2 = 1     # 点击后
w3 = 0.5   # 移动点击时长
w4 = 5     # 刷新页面后/点击弹窗后
# 尝试次数
n0 = 6

# 邮件收件人
add1 = "zy@szhorn.com"
add2 = "it02@szhorn.com"
add3 = "lidan@szhorn.com"
add4 = "zling@szhorn.com"
add5 = "lisa.qiu@szhorn.com"
add6 = "sys_dev@szhorn.com"  # 备用
add7 = "18802680909@163.com"  # 备用
add8 = "120000742@qq.com"  # 备用


def to_adds():
    adds = []
    adds.append(add1)
    # adds.append(add2)
    adds.append(add3)
    # adds.append(add4)
    # adds.append(add5)
    adds.append(add6)
    # adds.append(add7)
    # adds.append(add8)
    return adds