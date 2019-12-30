from datetime import datetime
from libs.config import conn, c


def create_db():
    # 建表
    sql = "CREATE TABLE CNIPA_PATENT_DATAS(ID VARCHAR2(200) PRIMARY KEY NOT NULL, TIVIEW VARCHAR2(500), APO VARCHAR2(200), APD Date, PN VARCHAR2(200), PD Date, ICST VARCHAR2(500), PAVIEW VARCHAR2(200), INVIEW VARCHAR2(200), PR VARCHAR2(200), PRD Date, AA VARCHAR2(500), AZ VARCHAR2(100), CPC VARCHAR2(500), ABVIEW1 VARCHAR2(4000), ABVIEW2 VARCHAR2(4000), WG_DESC1 VARCHAR2(4000), WG_DESC2 VARCHAR2(4000), CREATE_TIME Date, SOURCE VARCHAR2(100), RESERVE1 VARCHAR2(4000), RESERVE2 VARCHAR2(4000))"
    c.execute(sql)
    conn.commit()


def insert_db(db_dict):
    db_dict["create_time"] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    db_dict["source"] = "国家知识产权局专利检索"
    sql = "INSERT INTO CNIPA_PATENT_DATAS(ID, APO, TIVIEW, APD, PN, PD, ICST, PAVIEW, INVIEW, PR, PRD, AA, AZ, CPC, ABVIEW1, ABVIEW2, WG_DESC1, WG_DESC2, create_time, source) VALUES('{}', '{}', '{}', to_date('{}','yyyy.MM.dd'), '{}', to_date('{}', 'yyyy.MM.dd'), '{}', '{}', '{}', '{}', to_date('{}','yyyy.MM.dd'), '{}', '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd HH24:mi:ss'), '{}')".format(db_dict["ID"], db_dict["APO"], db_dict["TIVIEW"], db_dict["APD"], db_dict["PN"], db_dict["PD"], db_dict["ICST"], db_dict["PAVIEW"], db_dict["INVIEW"], db_dict["PR"], db_dict["PRD"], db_dict["AA"], db_dict["AZ"], db_dict["CPC"], db_dict["ABVIEW1"], db_dict["ABVIEW2"], db_dict["WG_DESC1"], db_dict["WG_DESC2"], db_dict["create_time"], db_dict["source"])
    c.execute(sql)
    conn.commit()


def select_companys():
    sql = "select COMPANY_NAME from CNIPA_PATENT_COMPANYS"
    results = c.execute(sql).fetchall()
    return results


def max_apd(PAVIEW):
    sql = "select max(APD) from CNIPA_PATENT_DATAS where PAVIEW='{}'".format(PAVIEW)
    try:
        max_apd_d = c.execute(sql).fetchone()[0]
    except:
        return
    return max_apd_d