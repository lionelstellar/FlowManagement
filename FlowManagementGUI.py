from tkinter import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk
import dbutils,Utils,sqlite3
import Monitor
from tkinter import messagebox
import os
LARGE_FONT = ("Helvetica", 20)
MID_FONT = ("Helvetica", 16)

db_path = dbutils.db_path
class Application(tk.Tk):
    def __init__(self):


        super().__init__()
        #置中
        self.wm_title("校园实验室流量管理系统")
        x = self.winfo_screenheight()
        y = self.winfo_screenwidth()
        x_ = 500
        yy = 700
        x1 = (y - x_) / 2
        y1 = (x - yy) / 2
        self.geometry("%dx%d+%d+%d" % (x_, yy, x1, y1))  # 设置窗口大小
        container = tk.Frame(self)
        container.pack(padx=25, pady=10)

        #数据库和json检查
        Utils.make_jsonfile()
        dbutils.checkDB(db_path)
        dbutils.checkTB('LabIP',db_path)
        dbutils.checkTB('Blacklist',db_path)

        self.frames = {}
        # 循环功能界面
        for F in (StartPage, A, B, C, D, A2, A3, B1, B2, B3, B4, C2, C3, D1, D2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # 切换，提升当前 tk.Frame z轴顺序（使可见）！！此语句是本程序的点睛之处

    def show_frame2(self, cont, ex1, ex2):
        frame = self.frames[cont]
        frame.tkraise()
        ex1.delete(0,END)
        ex2.delete(0, END)

    def show_frame3(self, cont,ex1):
        frame = self.frames[cont]
        frame.tkraise()
        ex1.delete(0,END)

    def show_frame4(self, cont, ex1, ex2, ex3, ex4):
        frame = self.frames[cont]
        frame.tkraise()
        ex1.delete(0,END)
        ex2.delete(0, END)
        ex3.delete(0,END)
        ex4.delete(0,END)

    def show_frame5(self, cont,ext,arg_name):

        if arg_name != 'Lab':
            messagebox.showinfo(title='提示', message="不为Lab")

        else:

            lab = ext.get()



            if not dbutils.check_pri_key("LabIP",lab):
                messagebox.showinfo(title='提示', message="您输入的Lab不存在，请重新输入！")
            else:
                Utils.set_arg(arg_name, lab)
                frame = self.frames[cont]
                frame.tkraise()

    def show_frame6(self, cont, ex, arg):

        frame = self.frames[cont]
        frame.tkraise()
        ex.delete(0, END)
        Utils.set_arg(arg,'')






class StartPage(tk.Frame):  #主页面
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="校园实验室流量管理系统", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=16)
        Button(self, text="A.实验室IP表管理", font=ft2, command=lambda: root.show_frame(A), width=20, height=3, fg="black", bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="B.实验室基本信息监控", font=ft2, command=lambda: root.show_frame(B), width=20, height=3).pack()
        Button(self, text="C.黑名单管理", font=ft2, command=lambda: root.show_frame(C), width=20, height=3, bg='gray', activebackground='black',activeforeground='white').pack()
        Button(self, text="D.实验室网络流量诊断", font=ft2, command=lambda: root.show_frame(D), width=20,height=3).pack()
        Button(self, text='E.退出系统', height=3, font=ft2, width=20, command=root.destroy, fg='black',bg='red',activebackground='black',activeforeground='white').pack()


class A(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="A.实验室IP表管理", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=16)
        Button(self, text="A1.实验室IP表查看", font=ft2, command=self.show_iptable, width=20, height=3, fg="black",
                   bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="A2.实验室IP表添加", font=ft2, command=lambda: root.show_frame(A2), width=20, height=3).pack()
        Button(self, text="A3.实验室IP表删除", font=ft2, command=lambda: root.show_frame(A3), width=20, height=3, bg='gray',
                   activebackground='black', activeforeground='white').pack()
        Button(self, text="A4.返回", height=3, font=ft2, width=20, command=lambda: root.show_frame(StartPage), fg='black', bg='red').pack()

    def show_iptable(self):
        # 数据库查询

        ret = Utils.show_table("LabIP")
        if ret != []:
            root = Tk()
            root.title("实验室IP表")
            tree = ttk.Treeview(root, show="headings")
            tree["columns"] = ("实验室", "IP", "用户", "口令")
            tree.column("实验室", width=150,anchor='center')  # 表示列,不显示
            tree.column("IP", width=150,anchor='center')
            tree.column("用户", width=150,anchor='center')
            tree.column("口令", width=150,anchor='center')
            tree.heading("实验室", text="实验室")  # 显示表头
            tree.heading("IP", text="IP")
            tree.heading("用户", text="用户")
            tree.heading("口令", text="口令")


            for i in range((len(ret))):  # 写入数据
                tree.insert('', i, values=ret[i])
            tree.pack(side=TOP, fill=BOTH, anchor='center')

        else:
            # 弹窗
            messagebox.showinfo(title='提示', message="实验室IP表为空")




class A2(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="A2.实验室IP表添加", font=LARGE_FONT)
        label.pack(pady=100)
        ft3 = tkFont.Font(size=14)
        ft4 = tkFont.Font(size=12)

        Label(self, text='实验室缩写：', font=ft3).pack(side=TOP)
        global e1, ee1
        e1 = StringVar()
        ee1 = Entry(self, width=20, textvariable=e1, font=ft3, bg='Ivory')
        ee1.pack(side=TOP)

        Label(self, text='实验室IP：', font=ft3).pack(side=TOP)
        global e2, ee2
        e2 = StringVar()
        ee2 = Entry(self, width=20, textvariable=e2, font=ft3, bg='Ivory')
        ee2.pack(side=TOP)

        Label(self, text='用户：', font=ft3).pack(side=TOP)
        global e10, ee10
        e10 = StringVar()
        ee10 = Entry(self, width=20, textvariable=e10, font=ft3, bg='Ivory')
        ee10.pack(side=TOP)

        Label(self, text='口令：', font=ft3).pack(side=TOP)
        global e11, ee11
        e11= StringVar()
        ee11 = Entry(self, width=20, textvariable=e11, font=ft3, bg='Ivory')
        ee11.pack(side=TOP)
        Button(self, text="返回(A)", width=8, font=ft4, command=lambda: root.show_frame4(A,ee1,ee2,ee10,ee11)).pack(pady=20)
        Button(self, text="确定添加", width=8, font=ft4, command=self.append).pack(side=TOP)

    def append(self):

        #数据库操作

        lab = str(e1.get())
        ip = str(e2.get())
        user = str(e10.get())
        password = str(e11.get())
        #print(lab,ip,user,password)
        if not Utils.isIP(ip):
            textvalue = 'ip不合法！'
        else:
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()
            vals = [lab,ip,user,password]
            curs, flag= dbutils.insert("LabIP",vals,curs)
            conn.commit()
            curs.close()
            if flag == False:
                textvalue = 'Lab已存在!'
            else:
                textvalue = '添加成功!'

        #弹窗
        messagebox.showinfo(title='提示', message=textvalue)


class A3(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="实验室IP表删除", font=LARGE_FONT)
        label.pack(pady=100)
        ft3 = tkFont.Font(size=14)
        ft4 = tkFont.Font(size=12)
        Label(self, text='实验室缩写：', font=ft3).pack(side=TOP)
        global e3, ee3
        e3 = StringVar()
        ee3 = Entry(self, width=20, textvariable=e3, font=ft3, bg='Ivory')
        ee3.pack()
        Label(self, text='实验室IP：', font=ft3).pack(side=TOP)
        global e4, ee4
        e4 = StringVar()
        ee4 = Entry(self, width=20, textvariable=e4, font=ft3, bg='Ivory')
        ee4.pack()
        Button(self, text="返回(A)", width=8, font=ft4, command=lambda: root.show_frame2(A, ee3, ee4)).pack(pady=20)
        Button(self, text="确定删除", width=8, font=ft4, command=self.delete).pack(side=TOP)

    def delete(self):
        #数据库操作
        #def delete(tb_name, curs, col, val):
        lab = str(e3.get())
        ip = str(e4.get())


        conn = sqlite3.connect(db_path)
        curs = conn.cursor()

        flag0 = 1

        if lab != '':
            col = 'Lab'
            val = lab
        elif ip != '':
            if not Utils.isIP(ip):
                textvalue = 'ip不合法！'
                flag0 = 0
            else:
                col = 'IP'
                val = ip
        else:
            textvalue = "输入为空！"
            flag0 = 0

        if flag0 == 1:
            curs, flag= dbutils.delete("LabIP",curs,col,val)
            conn.commit()
            curs.close()
            if flag == False:
                textvalue = '记录不存在'
            else:
                textvalue = '删除成功!'

        #弹窗
        messagebox.showinfo(title='提示', message=textvalue)

class B(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="B.实验室基本信息监控", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=14)
        ft3 = tkFont.Font(size=12)
        #print(Utils.get_arg("Lab"))
        Label(self, text='实验室缩写：', font=ft2).pack(side=TOP)
        global e5, ee5
        e5 = StringVar()
        ee5 = Entry(self, width=20, textvariable=e5, font=ft2, bg='Ivory')
        ee5.pack(side=TOP)


        Button(self, text="B1.查看网络连接", font=ft3, command=lambda: root.show_frame5(B1, e5, "Lab"), width=20, height=3,fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="B2.查看CPU", font=ft3, command=lambda: root.show_frame5(B2, e5, "Lab"), width=20, height=3).pack()
        Button(self, text="B3.查看进程", font=ft3, command=lambda: root.show_frame5(B3, e5, "Lab"), width=20, height=3, bg='gray',
               activebackground='black', activeforeground='white').pack()
        Button(self, text="B4.查看内存", font=ft3, command=lambda: root.show_frame5(B4, e5, "Lab"), width=20, height=3, bg='gray',
               activebackground='black', activeforeground='white').pack()
        Button(self, text='返回', height=3, font=ft3, width=20, command=lambda: root.show_frame3(StartPage, ee5),
               fg='black', bg='red').pack()




class B1(tk.Frame):
    lab = ''
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text="B1:实验室网络连接", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=12)
        Button(self, text="网络连接情况", font=ft2, command=self.show_conn, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        #666Button(self, text="断开与黑名单IP的网络连接", font=ft2, command=self.dlt_conn, width=20, height=3).pack()
        Button(self, text="返回(B)", font=ft2, command=lambda: root.show_frame(B), width=20, height=3, bg='gray',
               activebackground='black', activeforeground='white').pack()

    def show_conn(self):
        # 666：数据库查询，结果为str显示到文本框
        key = ["协议", "本地ip", "本地端口", "外部ip", "外部端口", "状态"]


        # 666：数据库查询，结果为str显示到文本框
        lab = Utils.get_arg("Lab")
        flag1, password = dbutils.find_value("LabIP", lab, "Password")
        flag2, ip = dbutils.find_value("LabIP", lab, "IP")
        flag3, user = dbutils.find_value("LabIP", lab, "User")
        # print(password,ip,flag1,flag2)
        if flag1 and flag2 and flag3:

            # 进程信息
            connetion_info = Monitor.os_connection(ip, user, password)
            if connetion_info == False:
                messagebox.showinfo(title='提示', message="网络连接超时")
            else:
                root = Tk()
                tree = ttk.Treeview(root, show="headings")

                root.title("%s实验室网络连接" % lab)

                tree["columns"] = ("协议", "本地ip", "本地端口", "外部ip", "外部端口", "状态")
                tree.column(key[0], width=100)  # 表示列,不显示
                tree.column(key[1], width=150)
                tree.column(key[2], width=100)
                tree.column(key[3], width=150)
                tree.column(key[4], width=100)
                tree.column(key[5], width=100)


                tree.heading(key[0], text=key[0])  # 显示表头
                tree.heading(key[1], text=key[1])
                tree.heading(key[2], text=key[2])
                tree.heading(key[3], text=key[3])
                tree.heading(key[4], text=key[4])
                tree.heading(key[5], text=key[5])
                for i in range((len(connetion_info))):  # 写入数据
                    tree.insert('', i, values=connetion_info[i])
                tree.pack(side=LEFT, fill=BOTH)
        else:
            messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)









    def dlt_conn(self):
        pass
        '''
        网络连接断开函数
        :return:
        '''


class B2(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text="B2:实验室CPU", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=12)
        Button(self, text="CPU使用情况", font=ft2, command=self.show_cpu, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="返回(B)", font=ft2, command=lambda : root.show_frame(B), width=20, height=3).pack()

    def show_cpu(self):
        key = ["用户空间", "内核空间", "空闲"]

        # 666：数据库查询，结果为str显示到文本框
        lab = Utils.get_arg("Lab")
        flag1, password = dbutils.find_value("LabIP", lab, "Password")
        flag2, ip = dbutils.find_value("LabIP", lab, "IP")
        flag3, user = dbutils.find_value("LabIP", lab, "User")
        # print(password,ip,flag1,flag2)
        if flag1 and flag2 and flag3:
            # CPU信息
            cpu_info = Monitor.os_cpu(ip, user, password)
            if cpu_info == False:
                messagebox.showinfo(title='提示', message="网络连接超时")
            else:
                root = Tk()
                tree = ttk.Treeview(root, show="headings")

                root.title("%s实验室cpu" % lab)

                tree["columns"] = (key[0], key[1], key[2])
                tree.column(key[0], width=100)  # 表示列,不显示
                tree.column(key[1], width=100)
                tree.column(key[2], width=100)


                tree.heading(key[0], text=key[0])  # 显示表头
                tree.heading(key[1], text=key[1])
                tree.heading(key[2], text=key[2])

                # 写入数据
                tree.insert('', 0, values=cpu_info)
                tree.pack(side=LEFT, fill=BOTH)
        else:
            messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)


class B3(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text="B3:实验室进程", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=12)
        Button(self, text="进程情况", font=ft2, command=self.show_pro, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="返回(B)", font=ft2, command=lambda : root.show_frame(B), width=20, height=3).pack()

    def show_pro(self):
        # 666：数据库查询，结果为str显示到文本框
        lab = Utils.get_arg("Lab")
        flag1, password = dbutils.find_value("LabIP", lab, "Password")
        flag2, ip = dbutils.find_value("LabIP",lab,"IP")
        flag3, user = dbutils.find_value("LabIP",lab,"User")
        #print(password,ip,flag1,flag2)
        if flag1 and flag2 and flag3:


            #进程信息
            process_info = Monitor.os_process(ip, user, password)
            if process_info == False:
                messagebox.showinfo(title='提示', message="网络连接超时")
            else:
                root = Tk()
                tree = ttk.Treeview(root, show="headings")

                root.title("%s实验室进程" % lab)

                tree["columns"] = ("用户", "进程id", "CPU占用率", "内存占用率", "开始时间", "命令")
                tree.column("用户", width=100)  # 表示列,不显示
                tree.column("进程id", width=100)
                tree.column("CPU占用率", width=100)
                tree.column("内存占用率", width=100)
                tree.column("开始时间", width=100)
                tree.column("命令", width=200)

                tree.heading("用户", text="用户")  # 显示表头
                tree.heading("进程id", text="进程id")
                tree.heading("CPU占用率", text="CPU占用率")
                tree.heading("内存占用率", text="内存占用率")
                tree.heading("开始时间", text="开始时间")
                tree.heading("命令", text="命令")
                for i in range((len(process_info))):  # 写入数据
                    tree.insert('', i, values=process_info[i])
                tree.pack(side=LEFT, fill=BOTH)
        else:
            messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令"%lab)


class B4(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        lab = Utils.get_arg("Lab")
        label = tk.Label(self, text="B4:实验室内存", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=12)
        Button(self, text="内存使用情况", font=ft2, command=self.show_mem, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="返回(B)", font=ft2, command=lambda : root.show_frame(B), width=20, height=3).pack()

    def show_mem(self):
        key = ["总共", "空闲中", "使用中", "缓存"]

        # 666：数据库查询，结果为str显示到文本框
        lab = Utils.get_arg("Lab")
        flag1, password = dbutils.find_value("LabIP", lab, "Password")
        flag2, ip = dbutils.find_value("LabIP", lab, "IP")
        flag3, user = dbutils.find_value("LabIP", lab, "User")
        # print(password,ip,flag1,flag2)
        if flag1 and flag2 and flag3:
            # MEM信息
            mem_info = Monitor.os_mem(ip, user, password)
            if mem_info == False:
                messagebox.showinfo(title='提示', message="网络连接超时")
            else:
                root = Tk()
                tree = ttk.Treeview(root, show="headings")

                root.title("%s实验室内存" % lab)

                tree["columns"] = (key[0], key[1], key[2], key[3])
                tree.column(key[0], width=100)  # 表示列,不显示
                tree.column(key[1], width=100)
                tree.column(key[2], width=100)
                tree.column(key[3], width=100)

                tree.heading(key[0], text=key[0])  # 显示表头
                tree.heading(key[1], text=key[1])
                tree.heading(key[2], text=key[2])
                tree.heading(key[3], text=key[3])

                 # 写入数据
                tree.insert('', 0, values=mem_info)
                tree.pack(side=LEFT, fill=BOTH)
        else:
            messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)


class C(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="C.IP黑名单管理", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=16)
        Button(self, text="C1.黑名单表查看", font=ft2, command=self.show_blacklist, width=20, height=3, fg="black",
                   bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="C2.黑名单IP添加", font=ft2, command=lambda: root.show_frame(C2), width=20, height=3).pack()
        Button(self, text="C3.黑名单IP删除", font=ft2, command=lambda: root.show_frame(C3), width=20, height=3, bg='gray',
                   activebackground='black', activeforeground='white').pack()
        Button(self, text="C4.返回", height=3, font=ft2, width=20, command=lambda: root.show_frame(StartPage), fg='black', bg='red').pack()

    def show_blacklist(self):
        # 666：数据库查询


        ret = Utils.show_table("Blacklist")
        if(ret != []):
            root = Tk()
            root.title("黑名单IP表")
            tree = ttk.Treeview(root, show="headings")
            tree["columns"] = ("黑名单IP", "时间")

            tree.column("黑名单IP", width=150)
            tree.column("时间", width=200)

            tree.heading("黑名单IP", text="黑名单IP")
            tree.heading("时间", text="时间")
            for i in range((len(ret))):  # 写入数据
                tree.insert('', i, values=ret[i])
            tree.pack(side=LEFT, fill=BOTH, anchor='center')
        else:
            # 弹窗
            messagebox.showinfo(title='提示', message="黑名单IP表为空")



class C2(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="C2.黑名单IP添加", font=LARGE_FONT)
        label.pack(pady=100)
        ft3 = tkFont.Font(size=14)
        ft4 = tkFont.Font(size=12)
        Label(self, text='黑名单IP：', font=ft3).pack(side=TOP)
        global e6, ee6
        e6 = StringVar()
        ee6 = Entry(self, width=20, textvariable=e6, font=ft3, bg='Ivory')
        ee6.pack()
        Button(self, text="返回(C)", width=8, font=ft4, command=lambda: root.show_frame3(C, ee6)).pack(pady=20)
        Button(self, text="确认添加", width=8, font=ft4, command=self.append).pack(side=TOP)


    def append(self):
        #数据库操作

        blackip = str(e6.get())

        if not Utils.isIP(blackip):
            textvalue = 'blackip不合法！'
        else:
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()
            vals = [blackip,Utils.getlocal()]
            curs, flag= dbutils.insert("Blacklist",vals,curs)
            conn.commit()
            curs.close()
            if flag == False:
                textvalue = 'BlackIP!'
            else:
                textvalue = '添加成功!'


        #弹窗
        messagebox.showinfo(title='提示', message=textvalue)


class C3(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="C3.黑名单IP删除", font=LARGE_FONT)
        label.pack(pady=100)
        ft3 = tkFont.Font(size=14)
        ft4 = tkFont.Font(size=12)
        Label(self, text='黑名单IP：', font=ft3).pack(side=TOP)
        global e7, ee7
        e7 = StringVar()
        ee7 = Entry(self, width=20, textvariable=e7, font=ft3, bg='Ivory')
        ee7.pack()
        Button(self, text="返回(C)", width=8, font=ft4, command=lambda: root.show_frame3(C, ee7)).pack(pady=20)
        Button(self, text="确认删除", width=8, font=ft4, command=self.delete).pack(side=TOP)

    def delete(self):
        #数据库操作
        #def delete(tb_name, curs, col, val):
        blackip = str(e7.get())



        conn = sqlite3.connect(db_path)
        curs = conn.cursor()


        curs, flag= dbutils.delete("Blacklist",curs,"BlackIP",blackip)
        conn.commit()
        curs.close()
        if flag == False:
            textvalue = '记录不存在'
        else:
            textvalue = '删除成功!'

        #弹窗
        messagebox.showinfo(title='提示', message=textvalue)


class D(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="D.网络流量诊断", font=LARGE_FONT)
        label.pack(pady=100)
        ft3 = tkFont.Font(size=16)
        Label(self, text='实验室缩写：', font=ft3).pack(side=TOP)
        global e8, ee8
        e8 = StringVar()
        ee8 = Entry(self, width=20, textvariable=e8, font=ft3, bg='Ivory')
        ee8.pack(side=TOP)
        Button(self, text="D1.SSH暴力破解检测", font=ft3, command=lambda: root.show_frame5(D1,e8,'Lab'), width=20, height=3, fg="black",
                   bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="D2.异常登录检测", font=ft3, command=lambda: root.show_frame5(D2,e8,'Lab'), width=20, height=3).pack()
        Button(self, text='返回(A)', height=3, font=ft3, width=20, command=lambda: root.show_frame3(StartPage, ee8), fg='black', bg='red').pack()


class D1(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        lab = Utils.get_arg("Lab")
        label = tk.Label(self, text="D1:实验室SSH暴力破解检测", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=12)
        ft3 = tkFont.Font(size=16)
        Label(self, text='设置失败次数阈值：', font=ft3).pack(side=TOP)
        global e13, ee13
        e13 = StringVar()
        ee13 = Entry(self, width=20, textvariable=e13, font=ft3, bg='Ivory')
        ee13.pack(side=TOP)


        Button(self, text="可疑IP检测结果", font=ft2, command=self.detect, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="检测结果一键加入黑名单", font=ft2, command=self.in_blacklist, width=20, height=3).pack()
        Button(self, text="返回(D)", font=ft2, command=lambda: root.show_frame6(D, ee13, "SSH_BF"), width=20, height=3, bg='gray',
               activebackground='black', activeforeground='white').pack()


    def detect(self):
        threshold = e13.get()
        if not Utils.isInt(threshold):
            messagebox.showinfo(title='提示', message="请输入整数")
        else:
            # 666：数据库查询，结果为str显示到文本框
            lab = Utils.get_arg("Lab")
            flag1, password = dbutils.find_value("LabIP", lab, "Password")
            flag2, ip = dbutils.find_value("LabIP", lab, "IP")
            flag3, user = dbutils.find_value("LabIP", lab, "User")
            # print(password,ip,flag1,flag2)
            if flag1 and flag2 and flag3:

                # 进程信息
                login_fail = Monitor.login_fail(ip, user, password, int(threshold))
                if login_fail == False:
                    messagebox.showinfo(title='提示', message="网络连接超时")
                elif len(login_fail) == 0:
                    messagebox.showinfo(title='提示', message="无可疑记录")
                else:
                    #将可疑ip写入json
                    blackip = []
                    for elem in login_fail:
                        blackip.append(elem[0])
                    Utils.set_arg("SSH_BF",blackip)

                    root = Tk()
                    tree = ttk.Treeview(root, show="headings")

                    root.title("%s实验室登录失败记录" % lab)
                    key = ["可疑IP", "失败次数"]
                    tree["columns"] = (key[0], key[1])
                    tree.column(key[0], width=150)  # 表示列,不显示
                    tree.column(key[1], width=50)


                    tree.heading(key[0], text=key[0])  # 显示表头
                    tree.heading(key[1], text=key[1])

                    for i in range((len(login_fail))):  # 写入数据
                        tree.insert('', i, values=login_fail[i])
                    tree.pack(side=LEFT, fill=BOTH)
            else:
                messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)

    def in_blacklist(self):
        blackip = Utils.get_arg("SSH_BF")
        if blackip == False:
            messagebox.showinfo(title='提示', message="没有需要加入黑名单的IP")
        elif len(blackip)== 0:
            messagebox.showinfo(title='提示', message="没有需要加入黑名单的IP")
        else:
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()
            success = []
            fail = []
            for elem in blackip:

                vals = [elem, Utils.getlocal()]
                curs, flag = dbutils.insert("Blacklist", vals, curs)
                if flag == False:
                    fail.append(elem)
                else:
                    success.append(elem)
            conn.commit()
            curs.close()
            textvalue = ''
            if len(success) > 0:
                textvalue += '，'.join(success) + "添加成功\n"
            if len(fail) > 0:
                textvalue += '，'.join(fail) + "已存在或添加失败"
            messagebox.showinfo(title='提示', message=textvalue)



class D2(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)

        label = tk.Label(self, text="D2.实验室异常时间登录检测", font=LARGE_FONT)
        label.pack(pady=100)
        ft2 = tkFont.Font(size=14)
        ft3 = tkFont.Font(size=12)
        Label(self, text='设置开始时间：\n（格式如：2019-03-09 00:00:00)', font=ft2).pack(side=TOP)
        global e9, ee9
        e9 = StringVar()
        ee9 = Entry(self, width=20, textvariable=e9, font=ft2, bg='Ivory')
        ee9.pack(side=TOP)

        Label(self, text='设置结束时间：\n（格式如：2019-03-09 00:00:00)', font=ft2).pack(side=TOP)
        global e12, ee12
        e12 = StringVar()
        ee12 = Entry(self, width=20, textvariable=e12, font=ft2, bg='Ivory')
        ee12.pack(side=TOP)

        Button(self, text="显示所有登录记录", font=ft3, command=self.show_result, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()

        Button(self, text="可疑IP检测结果", font=ft3, command=self.detect, width=20, height=3, fg="black",
               bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self, text="黑名单IP登陆检测", font=ft3, command=self.check_blackip, width=20, height=3).pack()
        Button(self, text="检测结果一键加入黑名单", font=ft3, command=self.in_blacklist, width=20, height=3).pack()
        Button(self, text="返回(D)", font=ft3, command=lambda: root.show_frame2(D, ee9, ee12)).pack(pady=20)

    def show_result(self):
        # 666：数据库查询，结果为str显示到文本框
        lab = Utils.get_arg("Lab")
        flag1, password = dbutils.find_value("LabIP", lab, "Password")
        flag2, ip = dbutils.find_value("LabIP", lab, "IP")
        flag3, user = dbutils.find_value("LabIP", lab, "User")
        # print(password,ip,flag1,flag2)
        if flag1 and flag2 and flag3:

            # 进程信息
            login_success = Monitor.login_success(ip, user, password)
            if login_success == False:
                messagebox.showinfo(title='提示', message="网络连接超时")
            else:
                root = Tk()
                tree = ttk.Treeview(root, show="headings")

                root.title("%s实验室登录记录" % lab)
                key = ["登录IP", "工作日", "登入时间", "登出时间"]
                tree["columns"] = ("登录IP", "工作日", "登入时间", "登出时间")
                tree.column(key[0], width=150)  # 表示列,不显示
                tree.column(key[1], width=50)
                tree.column(key[2], width=200)
                tree.column(key[3], width=200)


                tree.heading(key[0], text=key[0])  # 显示表头
                tree.heading(key[1], text=key[1])
                tree.heading(key[2], text=key[2])
                tree.heading(key[3], text=key[3])

                for i in range((len(login_success))):  # 写入数据
                    tree.insert('', i, values=login_success[i])
                tree.pack(side=LEFT, fill=BOTH)
        else:
            messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)

    def detect(self):
        # 666：数据库查询，结果为str显示到文本框
        starttime = e9.get()
        endtime = e12.get()
        #print(starttime,endtime)
        if not Utils.isVaildDate(starttime):
            messagebox.showinfo(title='提示', message="开始时间输入错误")
        elif not Utils.isVaildDate(endtime):
            messagebox.showinfo(title='提示', message="结束时间输入错误")
        elif starttime >= endtime:
            messagebox.showinfo(title='提示', message="开始时间晚于结束时间，请重新输入")
        else:
            lab = Utils.get_arg("Lab")
            flag1, password = dbutils.find_value("LabIP", lab, "Password")
            flag2, ip = dbutils.find_value("LabIP", lab, "IP")
            flag3, user = dbutils.find_value("LabIP", lab, "User")
            # print(password,ip,flag1,flag2)
            if flag1 and flag2 and flag3:

                login_success = Monitor.login_success(ip, user, password)



                if login_success == False:
                    messagebox.showinfo(title='提示', message="网络连接超时")
                else:

                    # 所有登陆写入json
                    all_login = []
                    for elem in login_success:
                        if elem[0] not in all_login:
                            all_login.append(elem[0])
                    Utils.set_arg("ALL_LOGIN", all_login)


                    record = []
                    for i in range((len(login_success))):  # 写入数据
                        if Utils.check_between(starttime,endtime,login_success[i][2],login_success[i][3]):
                            record.append(login_success[i])
                    if len(record) == 0:
                        messagebox.showinfo(title='提示', message="无异常登录！")
                    else:

                        # 异常时间登陆写入json
                        alert_login = []
                        for elem in record:
                            if elem[0] not in alert_login:
                                alert_login.append(elem[0])
                        Utils.set_arg("ALERT_LOGIN", alert_login)



                        root = Tk()
                        tree = ttk.Treeview(root, show="headings")

                        root.title("%s实验室登录记录" % lab)
                        key = ["登录IP", "工作日", "登入时间", "登出时间"]
                        tree["columns"] = ("登录IP", "工作日", "登入时间", "登出时间")
                        tree.column(key[0], width=150)  # 表示列,不显示
                        tree.column(key[1], width=50)
                        tree.column(key[2], width=200)
                        tree.column(key[3], width=200)

                        tree.heading(key[0], text=key[0])  # 显示表头
                        tree.heading(key[1], text=key[1])
                        tree.heading(key[2], text=key[2])
                        tree.heading(key[3], text=key[3])

                        for elem in record:
                            tree.insert('', i, values=elem)
                        tree.pack(side=LEFT, fill=BOTH)
            else:
                #pass
                messagebox.showinfo(title='提示', message="数据库查找不到%s实验室的ip或口令" % lab)
    def check_blackip(self):
        record = Utils.get_arg("ALL_LOGIN")
        if record == False:
            messagebox.showinfo(title='提示', message="没有黑名单内的IP登陆")
        elif len(record) == 0:
            messagebox.showinfo(title='提示', message="没有黑名单内的IP登陆")
        else:
            #查询blacklist表
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()

            dbutils.show_tb("Blacklist", curs)
            ret = curs.fetchall()
            conn.commit()
            curs.close()
            if ret == []:
                messagebox.showinfo(title='提示', message="没有黑名单内的IP登陆")
            else:
                blackip = []
                for elem in ret:
                    if elem[0] not in blackip:
                        blackip.append(elem[0])


                alert = []
                for elem in record:
                    if elem in blackip:
                        alert.append(elem)


                if len(alert) > 0:
                    textvalue = '，'.join(alert) + "是黑名单IP登陆\n"
                    messagebox.showinfo(title='提示', message=textvalue)
                else:
                    messagebox.showinfo(title='提示', message="没有黑名单内的IP登陆")



    def in_blacklist(self):
        blackip = Utils.get_arg("ALERT_LOGIN")
        if blackip == False:
            messagebox.showinfo(title='提示', message="没有需要加入黑名单的IP")
        elif len(blackip)== 0:
            messagebox.showinfo(title='提示', message="没有需要加入黑名单的IP")
        else:
            conn = sqlite3.connect(db_path)
            curs = conn.cursor()
            success = []
            fail = []
            for elem in blackip:

                vals = [elem, Utils.getlocal()]
                curs, flag = dbutils.insert("Blacklist", vals, curs)
                if flag == False:
                    fail.append(elem)
                else:
                    success.append(elem)
            conn.commit()
            curs.close()
            textvalue = ''
            if len(success) > 0:
                textvalue += '，'.join(success) + "添加成功\n"
            if len(fail) > 0:
                textvalue += '，'.join(fail) + "已存在或添加失败"
            messagebox.showinfo(title='提示', message=textvalue)


if __name__ == '__main__':



    # 实例化Application
    app = Application()
    app.show_frame(StartPage)
    # 主消息循环:
    app.mainloop()
