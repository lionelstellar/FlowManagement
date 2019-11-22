import time
import paramiko
import re
import Utils
def exec_cmd(host, user, password, cmdstr):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, 22, user, password)
        std_in, std_out, std_err = ssh_client.exec_command(cmdstr)


        stdout = std_out.read().decode()
        stderr = std_err.read().decode()

        if stderr != "":
            print(stderr)
            return False
        else:
            return stdout

    except OSError:
        return False
    else:
        return False



def os_process(host, user, password):
    #ret = exec_cmd(host, user, password, "top -n 1 -b")
    ret = exec_cmd(host, user, password, "ps -aux ")
    if ret == False:
        return False

    result=[]
    for elem in ret.split('\n')[1:-1]:
        tmp = []
        line = [ arg for arg in elem.split(' ') if arg != '']
        tmp.append(line[0])
        tmp.append(line[1])
        tmp.append(line[2])
        tmp.append(line[3])
        tmp.append(line[8])
        tmp.append(line[10])
        result.append(tmp)

    return result

def os_connection(host, user, password):

    ret = exec_cmd(host, user, password, "netstat -tu")
    if ret == False:
        return False

    dict={"CLOSED":"初始状态","LISTEN":"侦听状态","SYN_SEND":"发送等待","SYN_RECV":"打开连接","ESTABLISHED":"连接建立"}

    other = "关闭连接"
    result = []


    for line in ret.split('\n')[2:-1]:
        tmp = [ elem for elem in line.split(" ") if elem != '']

        record = []


        if '-' not in tmp[3] and '-' not in tmp[4]:
            record.append(tmp[0])
            record.append(tmp[3].split(':')[0])
            record.append(tmp[3].split(':')[1])
            record.append(tmp[4].split(':')[0])
            record.append(tmp[4].split(':')[1])
            if tmp[5] not in dict:
                record.append(other)
            else:
                record.append(dict[tmp[5]])

            result.append(record)

    return result

def os_cpu(host, user, password):
    # name = ["us(%)", "st(%)", "id(%)"]
    ret = exec_cmd(host, user, password, "top -b -n 1 ")
    ret = ret.split('\n')
    #print(ret)
    if ret == False:
        return False
    result = []
    for line in ret:
        if "%Cpu(s)" in line:
            l = line.split()
            # print(l)
            result.append(str(l[1].replace(",", '.')) + '%')
            result.append(str(l[3].replace(",", '.')) + '%')
            result.append(str(l[7].replace(",", '.')) + '%')
            return result

def os_mem(host, user, password):
    #name = ["total", "free", "used", "buff/cache"]
    ret = exec_cmd(host, user, password, "top -b -n 1")
    ret = ret.split('\n')
    if ret == False:
        return False
    val = []
    for line in ret:
        if "KiB Mem" in line:
            l = line.split()
            val.append(str(round(int(l[3])*1024/(10**6), 2)) + 'MB')
            val.append(str(round(int(l[5])*1024/(10**6), 2)) + 'MB')
            val.append(str(round(int(l[7])*1024/(10**6), 2)) + 'MB')
            val.append(str(round(int(l[-2])*1024/(10**6), 2)) + 'MB')
            # print(val)
            return val






def login_success(host, user, password):
    dict_month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                  "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dict_week = {"Mon":"星期一","Tue":"星期二","Wed":"星期三","Thu":"星期四","Fri":"星期五","Sat":"星期六","Sun":"星期日"}
    ret = exec_cmd(host, user, password, "last -f /var/log/wtmp.1")
    if ret == False:
        return False

    result = []
    for line in ret.split('\n'):

        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
        if ip:

            record = []
            ip = ip[0]
            #print(line)

            login_time = line.split(ip)[1].strip(' ').split('  ')[0]
            #login_time = line.split(ip)[1].strip(' ')

            weekday = dict_week[login_time.split(' ')[0]]
            #print("%"+login_time+"%")
            day = "2019-" + dict_month[login_time.split(' ')[1]] +"-"+ login_time.split(' ')[2]
            time = login_time.split(login_time.split(' ')[2])[1].strip(' ')
            if '-' in time:
                start_time = day + ' ' + time.split('-')[0].strip(' ') + ":00"
                end_time = day + ' ' + time.split('-')[1].strip(' ') + ":00"
                if(Utils.isVaildDate(start_time) and Utils.isVaildDate(end_time)):
                    record.append(ip)
                    record.append(weekday)
                    record.append(start_time)
                    record.append(end_time)

                    result.append(record)

    return result


def login_fail(host, user, password, threshold):
    dict_month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                  "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dict_week = {"Mon":"星期一","Tue":"星期二","Wed":"星期三","Thu":"星期四","Fri":"星期五","Sat":"星期六","Sun":"星期日"}
    ret = exec_cmd(host, user, password, "lastb | awk '{ print $3}' | sort | uniq -c | sort -n")
    result = []
    #ret = exec_cmd(host, user, password, "last -f /var/log/btmp")
    if ret == False:
        return False
    else:
        for line in ret.split('\n'):
            record = []
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            if ip != []:
                cnt = int(line.split(ip[0])[0].strip(' '))
                #print(cnt)
                if cnt > threshold and ip[0] != "127.0.0.1":
                    record.append(ip[0])
                    record.append(cnt)
                    result.append(record)
        return result




if __name__ == '__main__':

    #print(os_get_info('192.168.1.105', 'root', '`'))
    #print(os_get_network('192.168.1.105', 'root', '`'))
    #print(os_process('192.168.1.105', 'root', '`'))
    #print(os_connection('192.168.1.105', 'root', '`'))
    #print(login_success('192.168.1.105', 'root', '`'))
    #print(login_fail('192.168.1.105', 'root', '`'))
    #print(os_mem('192.168.1.106', 'root', '`'))
    #print(exec_cmd('192.168.1.106', 'root', '`', "top -n 1"))
    #print(os_get_file('192.168.1.105', 'root', '`',"CS"))
    pass

"""
要禁止一个IP，使用下面这条命令：

iptables -I INPUT -s ***.***.***.*** -j DROP

要解封一个IP，使用下面这条命令：

iptables -D INPUT -s ***.***.***.*** -j DROP
"""