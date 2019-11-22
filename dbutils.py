
#coding:utf-8
import sqlite3,os

db_path = './database/FlowManagement.db'
#确认数据库存在
def checkDB(db_path):
    if not os.path.exists(db_path):
        (filepath, filename) = os.path.split(db_path)
        os.system("mkdir -p %s" % filepath)
        os.system("touch %s" % db_path)
#查看所有表
def GetTables(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("select name from sqlite_master where type='table' order by name")
        return cur.fetchall()
    except:
            return False

def checkTB(name,db_path):
    ret = GetTables(db_path)
    if ret == False:
        return False
    else:
        if name not in ret:
            create_table(name,db_path)
            return True


#在bugdatabase数据库创建一个表
def create_table(name,db_path):
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    curs = conn.cursor()
    #建LabIP表
    if name == "LabIP":{
        curs.execute('''
            CREATE TABLE IF NOT EXISTS LabIP(
                Lab  PRIMARY KEY,
                IP TEXT,
                User TEXT,
                Password TEXT
            )
        ''')
    }
    # 建Blacklist表
    elif name == "Blacklist":{
        curs.execute('''
                    CREATE TABLE IF NOT EXISTS Blacklist(
                        BlackIP  PRIMARY KEY,
                        Time TEXT
                    )
                ''')
    }
    conn.commit()
    curs.close()

#插入
def insert(tb_name,vals,curs):
    #LabIP
    if tb_name == "LabIP" and len(vals)==4:
        query = 'INSERT INTO %s VALUES (?,?,?,?)' % tb_name
        try:
            curs.execute(query,vals)
            return curs,True
        except:
            return curs,False

    if tb_name == "Blacklist" and len(vals)==2:
        query = 'INSERT INTO %s VALUES (?,?)' % tb_name
        try:
            curs.execute(query,vals)
            return curs,True
        except:
            return curs,False
    else:
        # 表名错误
        return curs,False
#查看，返回列表，列表元素为记录形成的元组
def show_tb(tb_name,curs):
    if tb_name == "LabIP" or tb_name == "Blacklist":
        query = 'SELECT * FROM %s' % tb_name
        try:
            curs.execute(query)
            return curs, True
        except:
            return curs, False
    else:
        # 表名错误
        return curs, False

#按primary key删除
def delete(tb_name,curs,col, val):
    if tb_name == "LabIP" or tb_name == "Blacklist":

        #记录不存在
        query1 = 'SELECT * FROM %s WHERE %s="%s"'% (tb_name, col, val)
        if len(curs.execute(query1).fetchall()) < 1:
            return curs, False
        else:
            query = 'DELETE FROM %s WHERE %s="%s"' % (tb_name, col, val)

            try:
                #打印完整delete语句
                #print(query)
                curs.execute(query)
                return curs, True
            except ImportError:
                return curs, False
    else:
        # 表名错误
        return curs, False

def check_pri_key(tb_name,key):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    if tb_name == "LabIP":

        query = 'SELECT * FROM %s WHERE Lab="%s"'% (tb_name, key)
        #print(curs.execute(query).fetchall())
        if len(curs.execute(query).fetchall()) < 1:
            curs.close()
            return False

    elif tb_name == "Blacklist":

        query = 'SELECT * FROM %s WHERE BlackIP="%s"'% (tb_name, key)
        if len(curs.execute(query).fetchall()) < 1:
            curs.close()
            return False

    curs.close()
    return True


def find_value(tb_name,pri_key ,key):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    if tb_name == "LabIP":

        query = 'SELECT %s FROM %s WHERE Lab="%s"' % (key,tb_name, pri_key)
        if len(curs.execute(query).fetchall()) < 1:
            curs.close()
            return False,''
        else:
            return True,curs.execute(query).fetchall()[0][0]

    elif tb_name == "Blacklist":

        query = 'SELECT %s FROM %s WHERE BlackIP="%s"' % (key,tb_name, pri_key)
        if len(curs.execute(query).fetchall()) < 1:
            curs.close()
            return False,''
        else:
            return True,curs.execute(query).fetchall()[0][0]

    else:
        return False, ''






def main():

    checkDB(db_path)
    tb1 = "LabIP"
    tb2 = "Blacklist"
    checkTB(tb1,db_path)
    checkTB(tb2, db_path)
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()

    """
    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())
    
    curs, flag = insert(tb2, ("CS2", "192.168.1.105"), curs)
    print(flag)
    
    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())

    curs, flag = insert(tb1, ("my", "192.168.1.105", "jiangyikun", "`"), curs)
    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())
    conn.commit()
    curs.close()

    #a,b = find_value(tb1,"cs","Password")
    #print(b)

    #print(check_pri_key('LabIP','my'))
    """



    """
    #curs, flag = insert(tb1, ("my", "192.168.1.105", "jiangyikun", "`"), curs)
    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())
    


    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())





    curs, flag=delete(tb1,curs,"Lab","CS2")
    print(flag)



    curs,flag = show_tb(tb1,curs)
    print(curs.fetchall())

    
    """
    curs, flag = insert(tb2, ("192.168.1.102","2019-03-19 00:00:00"), curs)
    #curs, flag= delete(tb2,curs,"BlackIP","192.168.1.101")

    show_tb(tb2,curs)
    print(curs.fetchall())

    """
    
    
    conn.text_factory = str
   
    
    
    

    print("删除")
    curs, flag = delete(tb1, curs, "IP", "192.168.1.105")

    curs, flag = show_tb(tb1, curs)
    print(curs.fetchall())
    
    """
    conn.commit()
    curs.close()




if __name__ == '__main__':
    main()
