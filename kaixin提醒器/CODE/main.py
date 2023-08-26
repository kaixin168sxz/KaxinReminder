import tkinter as tk
from tkinter import ttk, messagebox
import kaixin as kx
import datetime as dt
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import threading
import sys
import calendar
from datetime import datetime
import os

if os.path.exists('.\\Data'):
    if os.path.isfile('.\\Data\\SaveFile.kx') and os.path.isfile('.\\Data\\images\\icon.ico') and os.path.isfile('.\\Data\\Users.kx'):
        print('OK')
    else:
        print('No File')
        sys.exit()
else:
    print('No .\\Data')
    sys.exit()

MainWindow = tk.Tk()
MainWindow.geometry('1000x300')
MainWindow.iconbitmap('.\\Data\\images\\icon.ico')
MainWindow.title('kaixin提醒器')
MainStyle = ttk.Style(MainWindow)
MainStyle.configure('TButton', font=('KaixinCodeFont', 20))
File = kx.Files('.\\Data\\SaveFile.kx')
DateList = ['月', '日', '时', '分']
DateDict = {'月': {'Big': 12, 'Small': 1}, '时': {'Big': 24, 'Small': 0}, '分': {'Big': 60, 'Small': 0}}
Close = False
UserFile = kx.Files('.\\Data\\Users.kx')
USER = eval(UserFile.read_file())
Window = False
DelWindowOpen = False
WindowOpen = False
AllWindows = 0
WindowsList = [False, False]

global AddWindow, Reminder, LookWindow, IsOK, dtree, tree, ReminderDict, NOW_USER, NAME, PASSWORD, CLOSE_PASSWORD, Info, DelWindow, SignUpWindow, SetUserWindow, User, LN, LPW, LoginWindow


def UpdateUser():
    global NOW_USER, ReminderDict, USER
    USER = eval(UserFile.read_file())
    NOW_USER = USER[0]
    print(NOW_USER)
    print(UserFile.read_file())
    if NOW_USER[1]:
        ReminderDict = eval(File.read_file())[NOW_USER[0]]


UpdateUser()


def Save():
    SaveData = eval(File.read_file())
    print(type(ReminderDict))
    SaveData[NOW_USER[0]] = ReminderDict
    File.save_file(str(SaveData))


def Close_DelWindow():
    global DelWindowOpen, DelWindow
    DelWindow.destroy()
    DelWindowOpen = False


def Del(Str, Password):
    global ReminderDict
    if Password == eval(UserFile.read_file())[1][NOW_USER[0]]:
        GetStr = Str.replace('月', ': ').replace('日', ': ').replace('时', ': ').replace('分', ': ').split(': ')
        try:
            ReminderDict[f"{{'月': '{GetStr[0]}', '日': '{GetStr[1]}', '时': '{GetStr[2]}', '分': '{GetStr[3]}'}}"]
        except KeyError:
            try:
                ReminderDict[f"{{'月': '{GetStr[0]}', '日': '{GetStr[1]}', '时': '{GetStr[2]}', '分': '{GetStr[3]}'}} (已提醒)"]
            except KeyError:
                print(':(')
            else:
                del ReminderDict[f"{{'月': '{GetStr[0]}', '日': '{GetStr[1]}', '时': '{GetStr[2]}', '分': '{GetStr[3]}'}} (已提醒)"]
        else:
            del ReminderDict[f"{{'月': '{GetStr[0]}', '日': '{GetStr[1]}', '时': '{GetStr[2]}', '分': '{GetStr[3]}'}}"]

        Save()
        messagebox.showinfo('提示', '已删除成功！')
        Close_DelWindow()
    else:
        messagebox.showinfo('提示', '请输入正确的密码')


def doubleClick(event):
    global DelWindowOpen, DelWindow
    e = event.widget
    iid = e.identify("item", event.x, event.y)
    try:
        for _ in [e.item(iid, "values")[0], e.item(iid, "values")[1]]:
            pass
    except KeyboardInterrupt:
        pass
    except IndexError:
        pass
    else:
        if not DelWindowOpen:
            Time = e.item(iid, "values")[0]
            Text = e.item(iid, "values")[1]
            outputStr = f'时间：{Time}\n内容：{Text}'
            DelMessage = messagebox.askquestion('删除', f'是否删除提醒：\n{outputStr}')
            if DelMessage == 'yes':
                DelWindow = tk.Tk()
                DelWindowOpen = True
                DelWindow.iconbitmap('.\\Data\\images\\icon.ico')
                DelWindow.title('kaixin提醒器')
                DelWindow.protocol('WM_DELETE_WINDOW', Close_DelWindow)
                DelWindow.geometry('300x125')
                DelWindow.resizable(False, False)
                tk.Label(DelWindow, text='请输入账号密码：', font=('KaixinCodeFont', 20)).pack()
                PassWord = ttk.Entry(DelWindow, show='*')
                PassWord.pack(fill=tk.X, expand=True, padx=10, pady=10)
                ttk.Button(DelWindow, text='确认', command=lambda: Del(Time, PassWord.get())).pack(fill=tk.BOTH, expand=True, padx=10)


def SaveAdd():
    global IsOK, DateDict, Window
    IsOK = True
    DateSaveDict = {}
    for Date in DateList:
        DateSaveDict[Date] = globals()['Time' + Date].get()
    if not str(DateSaveDict) in ReminderDict:
        for Date in DateList:
            if globals()['Time' + Date].get().isdigit():
                pass
            else:
                IsOK = False
        if IsOK:
            today = dt.date.today()
            if DateDict['月']['Small'] <= int(globals()['Time月'].get()) <= DateDict['月']['Big']:
                DateDict['日'] = {'Big': calendar.monthrange(today.year, int(globals()['Time月'].get()))[1], 'Small': 1}
            else:
                IsOK = False
            if IsOK:
                for Date in DateList:
                    globals()['Time1' + Date] = str(int(globals()['Time' + Date].get()))
                    if DateDict[Date]['Small'] <= int(globals()['Time1' + Date]) <= DateDict[Date]['Big']:
                        pass
                    else:
                        IsOK = False
                if IsOK:
                    ReminderDict[str(DateSaveDict)] = {'Time1': DateSaveDict, 'Reminder': Reminder.get()}
                    Save()
                    Window = False
                    AddWindow.destroy()
        if not IsOK:
            messagebox.showerror('错误', '日期格式错误！')
    else:
        messagebox.showinfo('已存在', '提醒时间已存在')

    return IsOK


def Close_AddWindow():
    global Window
    Close_AddWindow_Button = messagebox.askyesnocancel("提示", "是否保存且关闭？")
    if Close_AddWindow_Button:
        SaveAdd()
        Window = False
        AddWindow.destroy()
    elif Close_AddWindow_Button is None:
        pass
    else:
        Window = False
        AddWindow.destroy()


def show_window():
    MainWindow.deiconify()


def quit_window():
    global Close
    icon.stop()
    Close = True


def GetCalendar():
    Day = datetime.now()
    return eval(f"{{'月':'{Day.month}', '日':'{Day.day}', '时':'{Day.hour}', '分':'{Day.minute}'}}")


print(GetCalendar())
print(type(GetCalendar()['月']))


def Close_InfoWindow(Windows):
    global CLOSE_PASSWORD
    if globals()[f'Info{Windows}CLOSE_PASSWORD'].get() == eval(UserFile.read_file())[1][NOW_USER[0]]:
        globals()[f'Info{Windows}'].destroy()
    else:
        messagebox.showinfo('提示', '请输入正确的账号密码')


def Run():
    global CLOSE_PASSWORD, Info, AllWindows
    Calendar = GetCalendar()
    if Close:
        MainWindow.destroy()
        MainWindow.quit()
        sys.exit()
    if NOW_USER[1]:
        Now = str(Calendar)
        if Now in ReminderDict:
            print('In')
            if ReminderDict[Now]['Time1'] == Calendar:
                Windows = AllWindows
                globals()[f'Info{Windows}'] = tk.Tk()
                AllWindows += 1
                globals()[f'Info{Windows}'].iconbitmap('.\\Data\\images\\icon.ico')
                globals()[f'Info{Windows}'].title('kaixin提醒器')
                globals()[f'Info{Windows}'].resizable(False, False)
                globals()[f'Info{Windows}'].protocol('WM_DELETE_WINDOW', lambda: Close_InfoWindow(Windows))
                globals()[f'Info{Windows}'].wm_attributes("-topmost", 1)
                tk.Label(globals()[f'Info{Windows}'], text=f'''时间：{Now.replace("{", "").replace("}", "").replace("'", "").replace(": ", "").replace("时间", "")}''', font=('楷体', 20)).pack()
                tk.Label(globals()[f'Info{Windows}'], text=f'内容：{ReminderDict[Now]["Reminder"]}', font=('楷体', 20)).pack()
                tk.Label(globals()[f'Info{Windows}'], text='\n账号密码：', font=('楷体', 25)).pack()
                globals()[f'Info{Windows}CLOSE_PASSWORD'] = ttk.Entry(globals()[f'Info{Windows}'], font=('仿宋', 15), show='*')
                globals()[f'Info{Windows}CLOSE_PASSWORD'].pack(fill=tk.X, expand=True)
                ttk.Button(globals()[f'Info{Windows}'], text='确认', command=lambda: Close_InfoWindow(Windows)).pack()
                icon.notify(ReminderDict[Now]['Reminder'], "提醒")
                print(ReminderDict[Now]['Reminder'])
                ReminderDict[Now + ' (已提醒)'] = ReminderDict.pop(Now)
                ReminderDict[Now + ' (已提醒)']['Reminder'] = str(
                    ReminderDict[Now + ' (已提醒)']['Reminder']) + ' (已提醒)'
                Save()
        for Data in list(ReminderDict.keys()):
            ReminderTimeData = ReminderDict[Data]['Time1']
            if ' (已提醒)' in Data:
                if int(ReminderTimeData['月']) != int(GetCalendar()['月']) or int(ReminderTimeData['日']) != int(
                        GetCalendar()['日']):
                    print('Del')
                    del ReminderDict[Data]
                    Save()
                    break
            else:
                cur_time = datetime.now()
                target_time = f'{cur_time.year}-{ReminderTimeData["月"]}-{ReminderTimeData["日"]} {ReminderTimeData["时"]}:{ReminderTimeData["分"]}:00'
                print(f'Time is {target_time}')
                format_pattern = '%Y-%m-%d %H:%M:%S'
                cur_time = cur_time.strftime(format_pattern)
                difference = (datetime.strptime(target_time, format_pattern) - datetime.strptime(cur_time,
                                                                                                 format_pattern))
                if difference.days < 0:
                    print(f'Yes AddIt After<Time-\n{Data}\n>')
                    Calendar1 = f"{{'月': '{ReminderTimeData['''月''']}', '日': '{ReminderTimeData['''日''']}', '时': '{ReminderTimeData['''时''']}', '分': '{ReminderTimeData['''分''']}'}}"
                    ReminderDict[str(Calendar1) + ' (已提醒)'] = ReminderDict.pop(str(Calendar1))
                    ReminderDict[str(Calendar1) + ' (已提醒)']['Reminder'] = str(
                        ReminderDict[str(Calendar1) + ' (已提醒)']['Reminder']) + ' (已提醒)'
                    Save()
                else:
                    print('No UnAddit UnAfter<Time>')
        for item in tree.get_children():
            tree.delete(item)

        for DataKey in ReminderDict:
            Data = ReminderDict[DataKey]
            print(Data)
            tree.insert("", tk.END, values=(
                f'{Data["Time1"]["月"]}月{Data["Time1"]["日"]}日{Data["Time1"]["时"]}时{Data["Time1"]["分"]}分',
                Data['Reminder']))
    MainWindow.after(1000, Run)


def Close_MainWindow():
    MainWindow.withdraw()


def Add():
    global ReminderDict, AddWindow, Reminder, Window
    if not Window:
        AddWindow = tk.Tk()
        Window = True
        AddWindow.iconbitmap('.\\Data\\images\\icon.ico')
        AddWindow.title('kaixin提醒器')
        AddWindow.geometry('500x300')
        AddStyle = ttk.Style(AddWindow)
        AddStyle.configure('TLabel', font=('楷体', 20))
        AddStyle.configure('TButton', font=('楷体', 20))
        AddWindow.protocol('WM_DELETE_WINDOW', Close_AddWindow)

        AddTimeLabel = ttk.Label(AddWindow, text='提醒时间:')
        AddTimeLabel.pack(fill='x', expand=True)
        AddButton = ttk.Button(AddWindow, text='添加提醒', command=SaveAdd)
        AddButton.pack(side='bottom', pady=10)
        Reminder = ttk.Entry(AddWindow, font=('仿宋', 20))
        Reminder.pack(side='bottom', fill='x', expand=True)
        AddReminderLabel = ttk.Label(AddWindow, text='提醒内容:')
        AddReminderLabel.pack(side='bottom', fill='x', expand=True)

        for Name in DateList:
            globals()['Time' + Name] = ttk.Entry(AddWindow, width=2, font=('仿宋', 20))
            globals()['Time' + Name].pack(side='left', fill='x', expand=True)
            ttk.Label(AddWindow, font=('仿宋', 20), text=Name).pack(side='left')
        AddWindow.mainloop()


def sign_up():
    global SignUpWindow
    if len(NAME.get()) <= 13:
        if len(NAME.get()) == 0:
            messagebox.showinfo('提示', '请输入账号名')
        else:
            if len(PASSWORD.get()) == 0:
                messagebox.showinfo('提示', '请输入密码')
            else:
                SaveUser = eval(UserFile.read_file())
                SaveUser[0][0] = NAME.get()
                SaveUser[0][1] = True
                SaveUser[1][NAME.get()] = PASSWORD.get()
                print(SaveUser)
                UserFile.save_file(str(SaveUser))
                SaveFile = eval(File.read_file())
                SaveFile[NAME.get()] = {}
                File.save_file(str(SaveFile))
                UpdateUser()
                Close_Window(0)
                if WindowOpen:
                    if USER[0][1]:
                        User.configure(text=f'当前用户：{USER[0][0]}')
                    else:
                        User.configure(text='[未登录]')
                main()
    else:
        messagebox.showinfo('提示', '账号名只可以有13个字')


def Close_Window(Win):
    global WindowsList, SignUpWindow, LoginWindow
    WindowsList[Win] = False
    if Win == 1:
        LoginWindow.destroy()
    elif Win == 0:
        SignUpWindow.destroy()


def SignUp():
    global NAME, PASSWORD, SignUpWindow, WindowsList
    if not WindowsList[0]:
        SignUpWindow = tk.Tk()
        WindowsList[0] = True
        SignUpWindow.iconbitmap('.\\Data\\images\\icon.ico')
        SignUpWindow.title('kaixin提醒器')
        SignUpWindow.protocol('WM_DELETE_WINDOW', lambda: Close_Window(0))
        tk.Label(SignUpWindow, text='账号名：', font=('KaixinCodeFont', 20)).pack(pady=10)
        NAME = ttk.Entry(SignUpWindow, font=('KaixinCodeFont', 15))
        NAME.pack(fill=tk.X, expand=True, pady=10)
        tk.Label(SignUpWindow, text='密码（用于登录和关闭/删除提醒）：', font=('KaixinCodeFont', 20)).pack(pady=10)
        PASSWORD = ttk.Entry(SignUpWindow, font=('KaixinCodeFont', 15), show='*')
        PASSWORD.pack(fill=tk.X, expand=True, pady=10)
        ttk.Button(SignUpWindow, text='注册', command=sign_up).pack()


def Close_SUWindow():
    global WindowOpen, SetUserWindow
    SetUserWindow.destroy()
    WindowOpen = False


def login():
    global LN, LPW, LoginWindow
    UF = eval(UserFile.read_file())
    print(UF[1].keys())
    if LN.get() in UF[1]:
        if LPW.get() == UF[1][LN.get()]:
            UF[0][0] = LN.get()
            UserFile.save_file(str(UF))
            UpdateUser()
            Close_Window(1)
            if WindowOpen:
                if USER[0][1]:
                    User.configure(text=f'当前用户：{USER[0][0]}')
                else:
                    User.configure(text='[未登录]')
            main()

        else:
            messagebox.showinfo('提示', '密码错误')
    else:
        messagebox.showinfo('提示', '账号不存在')


def Login():
    global LN, LPW, LoginWindow, WindowsList
    if not WindowsList[1]:
        LoginWindow = tk.Tk()
        WindowsList[1] = True
        LoginWindow.iconbitmap('.\\Data\\images\\icon.ico')
        LoginWindow.title('kaixin提醒器')
        LoginWindow.protocol('WM_DELETE_WINDOW', lambda: Close_Window(1))
        tk.Label(LoginWindow, text='账号名：', font=('KaixinCodeFont', 20)).pack()
        LN = ttk.Entry(LoginWindow, font=('KaixinCodeFont', 15))
        LN.pack()
        tk.Label(LoginWindow, text='密码：', font=('KaixinCodeFont', 20)).pack()
        LPW = ttk.Entry(LoginWindow, font=('KaixinCodeFont', 15), show='*')
        LPW.pack()
        ttk.Button(LoginWindow, text='登录', command=login).pack()


def SetUser():
    global WindowOpen, SetUserWindow, User
    if not WindowOpen:
        SetUserWindow = tk.Tk()
        WindowOpen = True
        SetUserWindow.iconbitmap('.\\Data\\images\\icon.ico')
        SetUserWindow.title('kaixin提醒器')
        SUStyle = ttk.Style(SetUserWindow)
        SUStyle.configure('TButton', font=('KaixinCodeFont', 20))
        SetUserWindow.geometry('700x300')
        SetUserWindow.protocol('WM_DELETE_WINDOW', Close_SUWindow)
        SetUserWindow.resizable(False, False)
        User = ttk.Label(SetUserWindow, font=('KaixinCodeFont', 20))
        if USER[0][1]:
            User.configure(text=f'当前用户：{USER[0][0]}')
        else:
            User.configure(text='[未登录]')
        User.pack(anchor=tk.NW)
        ttk.Button(SetUserWindow, text='注册新账号', command=SignUp).pack(fill=tk.X, expand=True)
        ttk.Button(SetUserWindow, text='登录账号', command=Login).pack(fill=tk.X, expand=True)


def main():
    global tree
    for widget in MainWindow.winfo_children():
        widget.destroy()
    if NOW_USER[1]:
        UpdateUser()
        ButtonsFrame = tk.Frame(MainWindow)
        UserFrame = tk.Frame(ButtonsFrame)
        MUser = ttk.Label(UserFrame, font=('KaixinCodeFont', 20))
        print(USER[0])
        if USER[0][1]:
            MUser.configure(text=USER[0][0])
        else:
            MUser.configure(text='[未登录]')
        UserButton = ttk.Button(UserFrame, text='管理用户', command=SetUser)
        MUser.pack(padx=10, pady=10, ipady=10, side=tk.LEFT)
        UserButton.pack(padx=10, pady=10, ipady=10, side=tk.LEFT)
        UserFrame.pack(padx=10, anchor=tk.NW, side=tk.LEFT)

        ButtonFrame = tk.Frame(ButtonsFrame)
        AddButton = ttk.Button(ButtonFrame, text='添加提醒', command=Add)
        AddButton.pack(padx=10, pady=10, ipady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)

        ButtonFrame.pack(side=tk.RIGHT, anchor=tk.NE)

        ButtonsFrame.pack(fill=tk.X)

        scrollBar = tk.Scrollbar(MainWindow)
        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(
            MainWindow,
            show="headings",
            yscrollcommand=scrollBar.set,
            columns=("时间", "内容"),
        )
        tree.bind("<Double-1>", doubleClick)

        scrollBar.config(command=tree.yview)

        tree.heading("时间", text="时间")
        tree.heading("内容", text="内容")

        for item in tree.get_children():
            tree.delete(item)

        for DataKey in ReminderDict:
            Data = ReminderDict[DataKey]
            print(Data)
            tree.insert("", tk.END, values=(
                f'{Data["Time1"]["月"]}月{Data["Time1"]["日"]}日  {Data["Time1"]["时"]}时{Data["Time1"]["分"]}分',
                Data['Reminder']))
        tk.Label(text='双击删除提醒', font=('楷体', 20)).pack(side=tk.BOTTOM)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)
    else:
        tk.Label(MainWindow, text='请先注册一个账号', font=('楷体', 20)).pack()
        ttk.Button(MainWindow, text='注册', command=SignUp).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


main()

menu = (MenuItem('显示', show_window, default=True), Menu.SEPARATOR, MenuItem('退出', quit_window))
image = Image.open(".\\Data\\images\\icon.ico")
icon = pystray.Icon("icon", image, "kaixin提醒器", menu)

Run()
MainWindow.protocol('WM_DELETE_WINDOW', Close_MainWindow)
threading.Thread(target=icon.run, daemon=True).start()
MainWindow.mainloop()
