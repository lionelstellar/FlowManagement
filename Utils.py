import re
import time,datetime
import dbutils,sqlite3,os
import json
db_path = dbutils.db_path

def isIP(ip):
    
    # 简单的匹配给定的字符串是否是ip地址,下面的例子它不是IPv4的地址，但是它满足正则表达式
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
        return True
    else:
        return False

def isBlackIP(ip):
    if not isIP(ip):
        return False

    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    curs = conn.cursor()
    curs,flag = dbutils.show_tb("Blacklist", curs)

    if flag == True:
        for (blackip, time) in curs.fetchall():
            #可以打印所有的blackip
            #print(blackip,time)
            if ip == blackip:
                conn.commit()
                curs.close()
                return True

    conn.commit()
    curs.close()
    return False

def isInt(s):
    if s.isdigit():
        return True
    else:
        return False

def show_table(tb_name):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()

    curs, flag= dbutils.show_tb(tb_name,curs)
    ret = curs.fetchall()

    conn.commit()
    curs.close()

    return ret

def set_arg(arg_name,arg_value):
    tmp_file= './tmp/tmp.json'
    if not os.path.exists(tmp_file):
        os.system('mkdir -p ./tmp')
        os.system('touch %s' % tmp_file)
        with open(tmp_file,'w') as f:
            f.write("{}")

    else:
        with open(tmp_file, 'r') as f:
            if f.read() == '':
                with open(tmp_file, 'w') as f2:
                    f2.write("{}")


    with open(tmp_file,'r',encoding='utf-8') as f:
        dict = json.loads(f.read())

    dict[arg_name] = arg_value
    #print(dict)
    with open(tmp_file,'w',encoding='utf-8') as f_in:
        json.dump(dict,f_in,indent=4)

#@return flag:找到为true，未找到为false
#@return value:值
def get_arg(arg_name):
    tmp_file = './tmp/tmp.json'
    if not os.path.exists(tmp_file):
        return False,'1'

    with open(tmp_file, 'r', encoding='utf-8') as f:
        dict = json.loads(f.read())

    if arg_name not in dict:
        return False,'2'
    else:
        return dict[arg_name]


def isVaildDate(date):
    try:
        time.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False





#@return str:2019-03-22 23:17:18
def getlocal():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#查看是否在有时间重合
def check_between(start,end,t1,t2):
    if t2 <=start or t1 >= end:
        return False
    else:
        return True





def make_jsonfile():
    if os.path.exists('./tmp/tmp.json'):
        os.system('rm ./tmp/tmp.json')


