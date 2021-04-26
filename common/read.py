# encoding: utf-8
# @Time    : 2021/3/31 6:21 下午
# @Author  : Sail
# @File    : read.py
# @Software: PyCharm
import sys
import datetime

import xlrd
import pymysql


def get_pstatus(i):
    tmp = {"测试中": 1, "测试完成": 2, "已上线": 3}
    return tmp.get(chan.row_values(i)[3])


def get_ptype(i):
    tmp = {"标准需求": 1, "验收需求": 2, "生产事故": 3, "线上bug": 4, "紧急发版": 5}
    return tmp.get(chan.row_values(i)[1])


def c(dateTime):
    print(dateTime)
    return xlrd.xldate.xldate_as_datetime(dateTime, 0).__format__("%Y-%m-%d")


def get_venusid(group, tmp):
    ret = group.split("-")[0]
    conn = pymysql.connect(host='192.168.2.92', port=3306, database='venus_datebase', user='root',
                           password='HmElIsBkPKQNmfN2', charset='utf8')
    sql = """
         select id from cdb_task where category_business = %s and category_product = %s and version = %s
    """
    curson = conn.cursor()
    ret = curson.execute(sql, (group.split("-")[0], group.split("-")[1], tmp))
    print(sql)
    return ret


# 互动-Android标准版-v7.5.1-融合版直播2期

def get_mantisid(tmp, group):
    conn = pymysql.connect(host='117.50.17.66', port=3306, database='bugtracker', user='mantis',
                           password='6EJt2RYnAYGPaL4z', charset='utf8')
    sql = """
            select id from mantis_project_version_table where  version = %s and 
            project_id in (select id from mantis_project_table where name = %s)
    
    """
    curson = conn.cursor()
    ret = curson.execute(sql, (tmp, group.split("-")[1]))
    return ret


execlPath = sys.path[0] + "/" + "5.xlsx"

book = xlrd.open_workbook(execlPath)

chan = book.sheet_by_name("产品库")


def haha():
    db = pymysql.connect("192.168.2.92", "root", "HmElIsBkPKQNmfN2", "qa_p")
    cursor = db.cursor()

    for i in range(3, chan.nrows):
        try:

            group = chan.row_values(i)[0]

            tmp = chan.row_values(i)[2]
            project = tmp.split("-")[1]
            version = tmp.split("-")[0]
            ptype = get_ptype(i)
            pstatus = get_pstatus(i)
            begindate = c(chan.row_values(i)[5])
            enddate = c(chan.row_values(i)[6])
            ticecount = int(chan.row_values(i)[7])
            anticecount = int(chan.row_values(i)[8])
            zhunrucount = int(chan.row_values(i)[9])
            zhunchucount = int(chan.row_values(i)[10])
            anzhuchucount = int(chan.row_values(i)[11])
            casecount = int(chan.row_values(i)[12])
            maobugcount = int(chan.row_values(i)[13])
            fistbugcount = int(chan.row_values(i)[14])
            weibugcount = int(chan.row_values(i)[15])
            sumbugcount = int(chan.row_values(i)[16])
            yiliubug = int(chan.row_values(i)[17])
            P1 = int(chan.row_values(i)[18])
            P2 = int(chan.row_values(i)[19])
            P3 = int(chan.row_values(i)[20])
            P4 = int(chan.row_values(i)[21])
            P5 = int(chan.row_values(i)[22])
            tiyanbug = int(chan.row_values(i)[23])
            changecount = int(chan.row_values(i)[24])
            reopenbug = int(chan.row_values(i)[25])
            spendtime = chan.row_values(i)[26]
            online = int(chan.row_values(i)[27])
            isonline = int(chan.row_values(i)[28])
            onlinecount = int(chan.row_values(i)[29])
            rollcount = int(chan.row_values(i)[30])
            pquest = chan.row_values(i)[31]
            remark = chan.row_values(i)[32]
            venusid = get_venusid(group, tmp)
            mantisid = get_mantisid(tmp, group)
            addtiem = datetime.date.today()
            sql = f"""INSERT INTO collect (`group`,project,version,ptype,pstatus,begindate,enddate,
                                            ticecount,anticecount,zhunrucount,zhunchucount,anzhuchucount,casecount,maobugcount,
                                            fistbugcount,weibugcount,sumbugcount,yiliubug,P1,P2,P3,
                                            P4,P5,tiyanbug,changecount,reopenbug,spendtime,`online`,
                                            isonline,onlinecount,rollcount,pquest,remark,addtiem,venusid,
                                            mantisid)
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,
                    %s)
                    """
            cursor.execute(sql, (
                group, project, version, ptype, pstatus, begindate, enddate, ticecount, anticecount, zhunrucount,
                zhunchucount,
                anzhuchucount, casecount, maobugcount,
                fistbugcount, weibugcount, sumbugcount, yiliubug, P1, P2, P3,
                P4, P5, tiyanbug, changecount, reopenbug, spendtime, online,
                isonline, onlinecount, rollcount, pquest, remark, addtiem, venusid,
                mantisid
            ))
        except Exception as e:
            print(group,project,version)
            sql = f"""INSERT INTO collect (`group`,project,version)
                                VALUES
                                (%s,%s,%s)
                                """
            cursor.execute(sql, (
                group, project, version
            ))

        # print(sql)
        db.commit()


if __name__ == '__main__':
    haha()
    # """
    #
    #     select id from mantis_project_version_table where  version = 'v7.5.1-融合版直播2期' and project_id in
    #      (select id from mantis_project_table where name = 'Android标准版')
    # """


