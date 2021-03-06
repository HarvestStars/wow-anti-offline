import win32gui
import win32api
import win32con
import time
import win32clipboard as w
import random
import sys
import signal

def SetAliasWindows():
    winsNumber = 0
    while True:
        win = win32gui.FindWindow(None, '魔兽世界')
        if win != 0:
            winsNumber += 1
            NameWithNumber = "魔兽世界%d" % (winsNumber)
            win32gui.SetWindowText(win, NameWithNumber)
            print("发现魔兽窗口,已成功将其改名为:",NameWithNumber)
        else:
            break
    return winsNumber

def Action():
    # 离线重进
    # win32api.keybd_event(13, 0, 0, 0)
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    # time.sleep(10)
    # win32api.keybd_event(13, 0, 0, 0)
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    # time.sleep(1)

    # 向左移动再向右移动 各0.5秒
    win32api.keybd_event(65, 0, 0, 0) #A键位码是65
    time.sleep(0.5)
    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(68, 0, 0, 0) #D键位码是68
    time.sleep(0.5)
    win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 按技能1
    win32api.keybd_event(51, 0, 0, 0)
    win32api.keybd_event(51, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(3)

    # 跳跃
    win32api.keybd_event(32, 0, 0, 0)  # space键位码是32
    win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    time.sleep(1)
    
def run(winNumber):
    n = 1
    while n <= winNumber:
        NameWithNumber = "魔兽世界%d" % (n)
        win = win32gui.FindWindow(None, NameWithNumber)
        if win != 0:
            win32gui.ShowWindow(win, win32con.SW_SHOWMINIMIZED)
            win32gui.ShowWindow(win, win32con.SW_SHOWNORMAL)
            win32gui.ShowWindow(win, win32con.SW_SHOW)
            win32gui.SetWindowPos(win, win32con.HWND_NOTOPMOST, 0, 0, 1920, 1080, win32con.SWP_SHOWWINDOW)#第二个参数是置顶，前两个数字是位置，后两个数字是大小，最后一个是显示
            win32gui.SetForegroundWindow(win)  # 获取控制
            Action()
            win32gui.SetWindowText(win, '魔兽世界')
        else:
            print('找不到该窗口,确保游戏在独立窗口' % NameWithNumber)
        n += 1


#----------------------------------------------------------------------------Main Process----------------------------------------------------------------------------------------------
def handler(): 
    try:
        print("欢迎使用wow防离线工具, 请输入以下数字以执行指令:")
        print("1: 启动防离线程序")
        print("2: 退出程序")
        cmd = input()
        if cmd == "1":
            # step 1, 将所有窗口还原为魔兽世界  
            i = 0
            while i < 100:  #撑死100开吧?
                NameWithNumber = "魔兽世界%d" % (i)
                win = win32gui.FindWindow(None, NameWithNumber)
                if win !=0: 
                    print("发现未还原名称的魔兽窗口:", NameWithNumber, "立刻将其还原为 魔兽世界。")
                    win32gui.SetWindowText(win, '魔兽世界')
                else:
                    i+=1

            while True:
                print("new loop begin.")
                # step 2, 将所有窗口有序重名 1,2,3,4......n   
                winsNumber = SetAliasWindows()

                # step 3, loop for running
                run(winsNumber)
                
                # step 4, 每次loop结束停顿一段时间t, t<离线时间, 最好设置t为随机数
                A = 0
                B = 1
                a = random.uniform(A,B)
                C = 2 #小数精度
                # 选取0~1之间的随即小数作为base, 然后拉长到0~300秒
                t = round(a,C) * 300
                print("本次随机间隔为:",t)
                time.sleep(t)
        elif cmd == "2":
            sys.exit(0)
    except KeyboardInterrupt:
        handler()

handler()