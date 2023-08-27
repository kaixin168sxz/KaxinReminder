import sys
import xlwt
import tkinter as tk
import xlrd
import threading
import pystray
import datetime
from PIL import Image
from tkinter import messagebox
import time
from pathlib import Path

kais = time.time()
aaa = tk.Tk()
aaa.geometry('650x660+600+230')
aaa.iconbitmap('1233.ico')
aaa.title('kaixin')
aaa.resizable(False, False)  # 主窗口不能更改大小
k6 = tk.Label(aaa, text='', font=('宋体', 10), fg='red')
k6.place(x=0, y=640)

cnn = 15
libiao2 = []
libiao3 = []
libiao4 = []
anjian5 = []
tui22 = []
global aa11, shanc, aa22, shanc2
dhg = False
dhg1 = False
dhg3 = False
exit_program = False

now = datetime.datetime.now()
month12 = now.month
year12 = now.year
day12 = now.day
hour = now.hour



def click_menu(icon, item):  # 显示窗口
    print("点击了", item)
    aaa.deiconify()


def on_exit(icon, item):  # 调用这个之前是关闭tk窗口的功能，但是这个函数是子进程运行的，tk是在主进程中运行的，关闭tk在线程测试中会出现无法终止的现象，
    # 所以这个函数只修改全局变量xit_program = True，通过aaa.after(1000, check_exit)定时器来调用主进程的函数 check_exit函数来关闭tk窗口
    global exit_program
    exit_program = True
    icon.stop()
    # icon.visible = False


def notify(icon: pystray.Icon):  # # 定义通知内容的回调函数
    icon.notify(title="通知标题", message="通知内容")


def tubiao():  # 调用这个函数，任务栏出现图标，小图标的入口函数
    icon.run()


def gaunbi0():  # 调用这个函数，隐藏主窗口

    aaa.withdraw()


def gaunbi1():  # 销毁添加窗口的函数
    global dhg
    print('销毁窗口')
    aa11.destroy()
    dhg = False


def aa1():  # 点击添加 按键

    global aa11, dhg, anjian5
    anjian5 = []
    if not dhg:
        print('创建窗口')
        aa11 = tk.Tk()
        aa11.geometry('500x200+700+400')
        aa11.resizable(False, False)
        aa11.iconbitmap('1233.ico')
        aa11.title('添加信息')
        dhg = True
        aa11.protocol("WM_DELETE_WINDOW", gaunbi1)

        zz0 = tk.Label(aa11, text='你好,请输入对应的信息', font=('宋体', 12))

        zz0.place(x=20, y=20)
        zz1 = tk.Label(aa11, text='月份:', font=('宋体', 12))
        zz1.place(x=20, y=60)
        ryi0 = tk.Entry(aa11, width=4, font=('宋体', 12))
        ryi0.place(x=65, y=60)
        ryi0.insert(0, str(month12))
        anjian5.append(ryi0)

        zz1 = tk.Label(aa11, text='日期:', font=('宋体', 12))  # 日期文本及输入框，已及ryi0返回加入anjian5列表
        zz1.place(x=120, y=60)
        ryi1 = tk.Entry(aa11, width=4, font=('宋体', 12))
        ryi1.place(x=165, y=60)

        anjian5.append(ryi1)
        zz2 = tk.Label(aa11, text='小时:', font=('宋体', 12))  # 小时文本及输入框，已及ryi0返回加入anjian5列表
        zz2.place(x=220, y=60)
        ryi2 = tk.Entry(aa11, width=4, font=('宋体', 12))
        ryi2.place(x=265, y=60)
        anjian5.append(ryi2)

        zz3 = tk.Label(aa11, text='分钟:', font=('宋体', 12))  # 小时文本及输入框，已及ryi0返回加入anjian5列表
        zz3.place(x=320, y=60)
        ryi3 = tk.Entry(aa11, width=4, font=('宋体', 12))
        ryi3.place(x=365, y=60)
        anjian5.append(ryi3)
        ryi3.insert(0, '00')

        zz4 = tk.Label(aa11, text='事件:', font=('宋体', 12))  # # 事件文本及输入框，已及ryi0返回加入anjian5列表
        zz4.place(x=20, y=100)
        ryi4 = tk.Entry(aa11, width=50, font=('宋体', 12))
        ryi4.place(x=65, y=100)
        anjian5.append(ryi4)

        dd81 = tk.Button(aa11, text='添 加', font=('宋体', 12), width=10, command=rss56)  # 创建按钮 width宽度 command绑定函数
        dd81.place(x=200, y=165)  # 使用坐标显示

        aa11.mainloop()  # 显示窗口
    else:
        print('存在窗口')
        gaunbi1()


def gaunbi2():  # 销毁删除窗口的函数
    global dhg1
    print('销毁窗口')
    aa22.destroy()
    dhg1 = False


def gaunbi3(nb81, root2):  # 点击关闭提醒小窗口后执行这个函数
    global dhg3
    ak36 = nb81.get()

    if ak36 == "c":
        root2.destroy()
    else:
        nb82 = tk.Label(root2, text=f'关闭码错误', font=('宋体', 10), fg='red')  # 定义初始的zz5变量
        nb82.place(x=10, y=200)  # 坐标


def aa2():  # 点击 删除 执行的函数
    global aa22, dhg1, shanc, shanc2
    if not dhg1:
        if len(libiao4) > 0:
            print('创建窗口')
            aa22 = tk.Tk()
            aa22.geometry('500x200+700+400')
            aa22.resizable(False, False)
            aa22.iconbitmap('1233.ico')
            aa22.title('删除信息')
            dhg1 = True
            aa22.protocol("WM_DELETE_WINDOW", gaunbi2)
            yy0 = tk.Label(aa22, text=f'{" " * 1}你好，请输入需要删除的序列号，如 1 ', font=('宋体', 12))
            yy0.place(x=20, y=20)
            yy1 = tk.Label(aa22, text=f'请输入序列号:', font=('宋体', 12))
            yy1.place(x=35, y=60)
            shanc = tk.Entry(aa22, width=5, font=('宋体', 16))
            shanc.place(x=160, y=60)
            yy9 = tk.Label(aa22, text=f'输入删除密码:', font=('宋体', 12))
            yy9.place(x=35, y=100)
            shanc2 = tk.Entry(aa22, width=5, font=('宋体', 16))
            shanc2.place(x=160, y=100, )

            yy2 = tk.Button(aa22, text='确认删除', font=('宋体', 12), width=10,
                            command=a88p)
            yy2.place(x=200, y=150)
            print(libiao4)
            aa22.mainloop()
        else:
            pass
    else:
        print('存在窗口')


def a88p():  # 主要功能就是删除用的
    global cnn, libiao2, kaiguan, ip00, ghj02
    vmt8 = len(libiao4)
    ek8 = shanc.get()
    ek9 = shanc2.get()
    try:
        if int(float(ek8)) <= vmt8 and type(int(float(ek8))) == int:  # 这个判断防止删除不存在列表内的元素而报错，比如列表为空了，还在删除
            if ek9 == 'm':

                rtu01 = messagebox.askquestion("确认窗口",
                                               f"你确定要删除{int(float(ek8))}{libiao4[int(float(ek8)) - 1]}号吗？")

                if rtu01 == 'yes':

                    libiao4.pop(int(float(ek8)) - 1)
                    shanc.delete(0, 'end')
                    gaunbi2()

                    for widget in aaa.winfo_children():  # 清空aaa屏幕上的标签

                        if isinstance(widget, tk.Label):

                            widget.config(text="")
                    libiao2 = libiao4
                    print('用户点击了确认')
                    cnn = 15
                    zuihou()
                    xieru85()
                    kaiguan = True
                    ip00 = 0
                    ghj02 = True

                else:
                    print('用户点击了取消')
                    gaunbi2()  # 销毁窗口
            else:
                yy8 = tk.Label(aa22, text=f'密码错误', font=('宋体', 16), fg='red')
                yy8.place(x=240, y=100)

        else:
            print('数字太大')
            yy7 = tk.Label(aa22, text=f'输入数字过大', font=('宋体', 16), fg='red')
            yy7.place(x=240, y=60)
    except ValueError:
        print("字符串无法转换为浮点数")
        yy7 = tk.Label(aa22, text=f'无法转换数字', font=('宋体', 16), fg='red')
        yy7.place(x=240, y=60)


hui = False


def rss56():  # 主要作用是添加数据用的，添加进表格
    global tui22, cnn, libiao2, hui, kaiguan, ip00, ghj02

    tui22 = []

    complete_data = True
    zz5 = tk.Label(aa11, text='', font=('宋体', 18))
    zz5.place(x=150, y=135)  # 坐标

    for i2p in range(len(anjian5)):  # 对之前的anjian5列表解析出真正的输入框数据
        hpp = anjian5[i2p].get()
        tui22.append(hpp)

        if len(hpp) == 0:  # 如果hpp存在等于0的情况，就相当于没有输入信息
            complete_data = False  # 变量设置为假
            zz5.config(text='请输入完整的数据', fg='red')

            break  # 有一项没输入就可以提示返回了，节省资源
    riqi85 = f'{year12}.{tui22[0]}.{tui22[1]}'
    date_format = "%Y.%m.%d"
    try:
        datetime.datetime.strptime(riqi85, date_format)
        print("字符串是一个有效的日期。")
        hui = True
    except ValueError:
        print("字符串不是一个有效的日期。")
        hui = False

    if complete_data:  # 如果全部输入框全部输入数据
        try:
            if month12 <= int(tui22[0]) <= 12 and int(tui22[1]) <= 31 and (0 <= int(
                    tui22[2]) <= 23) and int(
                tui22[3]) <= 60 and len(
                str(tui22[
                        4])) > 0 and hui == True:



                oledt = datetime.datetime(int(year12), int(tui22[0]), int(tui22[1]), int(tui22[2]), int(tui22[3]))
                newdt = datetime.datetime.now()
                if oledt > newdt:
                    print('大于真实时间')

                    rtu05 = messagebox.askquestion("确认窗口",
                                                   f"你确定要添加   {tui22[0]}月{tui22[1]}   {tui22[2]}时{tui22[3]}分  "
                                                   f"  {tui22[4]}   信息吗？")

                    if rtu05 == 'yes':

                        libiao4.append(
                            [80, f'{int(year12)}.{int(tui22[0])}.{int(tui22[1])}', f'{int(tui22[2])}:{int(tui22[3])}',
                             f'{tui22[4]}'])
                        print(f'{int(year12)}.{int(tui22[0])}.{int(tui22[1])}', f'{int(tui22[2])}:{int(tui22[3])}',
                              789000)

                        print(libiao4)
                        xieru85()
                        gaunbi1()
                        for widget in aaa.winfo_children():  # 清空aaa屏幕上的标签
                            # 检查子部件是否为标签
                            if isinstance(widget, tk.Label):
                                # 清空标签的文本内容
                                widget.config(text="")
                        libiao2 = []
                        print('用户点击了确认')
                        huoqushuju()
                        cnn = 15
                        zuihou()
                        kaiguan = True
                        ip00 = 0
                        ghj02 = True
                    else:
                        print('取消')
                        print(tui22)
                        gaunbi1()

                else:
                    print('小于真实时间')
                    zz5.config(text='不能提醒历史时间', fg='red')

            else:

                zz5.config(text='请输入正确的数据', fg='red')

        except ValueError:
            zz5.config(text='输入的不是个整数', fg='red')  # 提醒下



ty128 = ''
kaiguan = True
ip00 = 0
global target_date
ikp = 0
ghj02 = True
mfb82 = 0


def check_exit():  # 如果exit_program为真，销毁aaa窗口，退出aaa，exit退出程序
    global exit_program, target_date, ty128, kaiguan, ip00, i, now, ikp, libiao2, cnn, ghj02, cjuli12_plus_48h, mfb82
    if len(libiao4) > 0:

        now = datetime.datetime.now()
        if ghj02:

            for km01 in libiao3:
                cjuli2 = f"{km01[1]} {km01[2]}"
                cjuli12 = datetime.datetime.strptime(cjuli2, "%Y.%m.%d %H:%M")
                cjuli12_plus_48h = cjuli12 + datetime.timedelta(minutes=5)
                print(km01, '列表的第一次时间')
                print(cjuli12_plus_48h, type(cjuli12_plus_48h), '加48小时后的时间')
                cjuli22_plus_48h = cjuli12_plus_48h.strftime("%Y.%m.%d %H:%M")

                k1 = tk.Label(aaa, text=f'自动删除序列1时间', font=('宋体', 10), fg='red')
                k1.place(x=525, y=615)  # 坐标
                k2 = tk.Label(aaa, text=f'{cjuli22_plus_48h}', font=('宋体', 10), fg='red')
                k2.place(x=525, y=635)  # 坐标

                ghj02 = False
                break
        if now > cjuli12_plus_48h:
            libiao3.pop(0)
            print('列表的第一次时间删除成功666')
            ghj02 = True
            # -----------------------------------------------------------------
            libiao2 = libiao3
            for widget in aaa.winfo_children():

                if isinstance(widget, tk.Label):

                    widget.config(text="")
            cnn = 15
            zuihou()
            xieru85()
        # ------------------------------------------------------------------
        if kaiguan:

            for i in libiao4:

                ty128 = f"{i[1]} {i[2]}"

                fh658 = datetime.datetime.strptime(ty128, '%Y.%m.%d %H:%M')
                fh659 = fh658.strftime("%Y.%m.%d %H:%M")

                if fh658 > now:
                    target_date = datetime.datetime.strptime(ty128, '%Y.%m.%d %H:%M')
                    kaiguan = False

                    aaa.title(f"下次提醒时间: {fh659}")
                    break
                else:
                    target_date = datetime.datetime.strptime(ty128, '%Y.%m.%d %H:%M')
                    print('ELSE列表里的时间小于真实的时间', target_date)
                    aaa.title(f"下次提醒时间: 暂无提醒时间")
                    kaiguan = 3
        # ---------------------------------------------------------------
        now = datetime.datetime.now()
        print(ip00, kaiguan, 99999)
        if now >= target_date and kaiguan != 3:
            notify(icon)
            if ip00 == 0:
                root2 = tk.Tk()
                root2.geometry('202x250+1650+300')
                # ----------------------------------------------------------------------------------
                for widget in aaa.winfo_children():

                    if isinstance(widget, tk.Label):

                        widget.config(text="")
                libiao2 = []
                print('用户点击了确认')
                huoqushuju()
                cnn = 15
                zuihou()
                ghj02 = True
            # ----------------------------------------------------------------------------------
            else:
                root2 = tk.Tk()
                root2.geometry('202x250+1700+360')

            root2.title('提醒')
            root2.resizable(False, False)
            ikp = ikp + 1
            root2.iconbitmap('1233.ico')
            root2.wm_attributes("-topmost", 1)
            nb78 = tk.Label(root2, text=f'{i[1]}    {i[2]}', font=('宋体', 14), fg='red')
            nb78.place(x=0, y=0)  # 坐标
            nb79 = tk.Label(root2, text=f'{i[3]}', font=('宋体', 14), wraplength=200, justify='left')
            nb79.place(x=0, y=50)
            nb78 = tk.Label(root2, text=f'关闭码:', font=('宋体', 10), fg='blue')
            nb78.place(x=10, y=220)  # 坐标
            nb81 = tk.Entry(root2, width=4, font=('宋体', 12), )
            nb81.place(x=70, y=220)
            a45 = tk.Button(root2, text='确认', font=('宋体', 10), width=8,
                            command=lambda: gaunbi3(nb81, root2))
            a45.place(x=130, y=220)  # 使用坐标显示
            root2.protocol("WM_DELETE_WINDOW", lambda: gaunbi3(nb81, root2))
            # 个参数是关闭多个小窗口的关键代码
            target_date += datetime.timedelta(minutes=1)
            ip00 = ip00 + 1
            if ip00 == 2:
                kaiguan = True

                ip00 = 0
            ghj02 = True

    if mfb82 == 99:
        mfb82 = 0

    k6.configure(text=f'{mfb82}')

    if exit_program:
        aaa.destroy()
        aaa.quit()
        sys.exit()  # 退出程序

    mfb82 = mfb82 + 1
    aaa.after(5000, check_exit)


def huoqushuju():
    pe0 = xlrd.open_workbook('123.xls')
    sheet = pe0.sheets()[0]
    for row in range(sheet.nrows):

        cell_value = sheet.row_values(row, )

        tt1 = datetime.datetime.strptime(cell_value[1], '%Y.%m.%d')
        tt2 = datetime.datetime.strftime(tt1, '%Y.%m.%d')
        h1, m1 = cell_value[2].split(':')
        hm1 = f'{h1.zfill(2)}:{m1.zfill(2)}'

        libiao2.append([int(cell_value[0]), tt2, hm1, cell_value[3]])


def xieru85():
    k = 0  # 行
    a = xlwt.Workbook()
    b = a.add_sheet('文档1')
    for ii58 in libiao4:

        d = 0  # 列
        for j in ii58:
            b.write(k, d, j)
            d = d + 1
        k = k + 1
    a.save('123.xls')


def xinxi00(r1, r2, r3, r4, r5, r6, r7):
    global cnn
    b1 = tk.Label(aaa, text=f'{r1}{" " * r5}{r2}{" " * 2}{r3}{" " * 2}{r4}{r7}', font=('宋体', 12), fg=r6)
    b1.place(x=20, y=cnn)
    b2 = tk.Label(aaa, text='-' * 152, font=('宋体', 6), )
    cnn = cnn + 20
    b2.place(x=16, y=cnn)
    cnn = cnn + 20


def zuihou():
    global libiao3, libiao4
    libiao3 = []
    libiao4 = []
    libiao3 = sorted(libiao2, key=lambda x: (x[1], x[2]))
    ioy = 1
    dh8852 = 1
    for i2 in libiao3:
        libiao4.append([ioy, i2[1], i2[2], i2[3]])
        ioy = ioy + 1
    for i in libiao4:
        if dh8852 <= 15:
            if i[0] < 10:
                kongge = 3
            else:
                kongge = 2
            dh8852 = dh8852 + 1
            zhenshi = datetime.datetime.now()
            cjuli = f"{i[1]} {i[2]}"  # 得到时间样式
            cjuli1 = datetime.datetime.strptime(cjuli, "%Y.%m.%d %H:%M")  # 转换为date样式
            weekday_name = cjuli1.strftime("%A")
            weekday_number = cjuli1.strftime("%w")
            if cjuli1 < zhenshi:  # 过期时间全部显示为红色
                cpt8 = 'red'  # 颜色
                fkb2 = f'(已提醒)'
            else:  # 不过期的执行这边的代码
                if weekday_name == "Saturday":  # 判断星期6
                    cpt8 = 'black'  # 颜色
                    fkb2 = '(星期六)'
                elif weekday_number == "0":  # 判断星期7
                    cpt8 = 'black'  # 颜色
                    fkb2 = '(星期日)'
                else:  # 其余情况执行这个
                    cpt8 = 'black'  # 黑色
                    fkb2 = ''
            xinxi00(i[0], i[1], i[2], i[3], kongge, cpt8, fkb2)  # 把参数传递给xinxi00函数，用来在tk上显示出来
    print(libiao4, 4)


# -----------------------------------

filename = "123.xls"  # 检测表格是否存在，不存在就创建
file_path = Path(filename)

if file_path.exists():
    print("文件已存在")
else:
    # 创建新的Excel文件
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("文档1")
    workbook.save(filename)
    print("文件已创建")
# -------------------------------------------
menu = (  # # 创建菜单项
    pystray.MenuItem('菜单A', click_menu),  # 第一个菜单项
    pystray.MenuItem(text='点击托盘图标显示', action=click_menu, default=True, visible=False),  # 第五个菜单项
    pystray.MenuItem(text='退出', action=on_exit),  # 最后一个菜单项
)
# 创建图标对象
image = Image.open("1233.ico")
icon = pystray.Icon("name", image, "提醒器", menu)
aaa.protocol("WM_DELETE_WINDOW", gaunbi0)
aaa.after(5000, check_exit)
ety = threading.Thread(target=tubiao, daemon=True)
ety.start()
huoqushuju()
zuihou()
a1 = tk.Button(aaa, text='添 加', font=('宋体', 16), width=10, command=aa1)
a1.place(x=130, y=615)
a2 = tk.Button(aaa, text='删 除', font=('宋体', 16), width=10, command=aa2)
a2.place(x=380, y=615)
aaa.mainloop()
