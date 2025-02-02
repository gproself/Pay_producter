from tkinter import *
from scapy.all import *
from plyer import notification
import time
import ctypes
import os
import threading
from tkinter import messagebox

last_notification_time = 0
ip_count = 0


def run_as_admin(exe_path):
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            os.startfile(exe_path)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)
    except:
        pass

def monitor_packet(packet):
    global last_notification_time, ip_count
    try:
        with open('pay_ips.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if any(line.strip() == packet[IP].src for line in lines): # type: ignore
            ip_count += 1
            print(packet[IP].src) # type: ignore
            current_time = time.time()
            if ip_count >= 3:
                if current_time - last_notification_time > 300:
                    run_as_admin(r'dns.exe')
                    notification.notify(
                        title='خرید شناسایی شد',
                        message='شما در سپر محافظت قرار گرفتید 🚀🚀',
                        app_name='سقف طلایی',
                        timeout=10
                    )
                    last_notification_time = current_time
                ip_count = 0
    except:
        pass

used = False

win = Tk()
win.geometry('900x700')
win.resizable(width='false', height='false')
win.title('protector')

bg_image = PhotoImage(file=r'bg.png')
button_image = PhotoImage(file=r'button.png')

bg = Label(win, image=bg_image)
button = Button(win, image=button_image, command=lambda: start())

bg.place(x=-2, y=0)
button.place(x=296, y=215)

def runed():
    sniff(filter="tcp", prn=monitor_packet, store=0)

def start():
    global used
    if used:
        messagebox.showerror('خطا','برنامه شروع شده!')
    else:
        used = True
        messagebox.showinfo('موفق','خدمات شروع شد!')
        threading.Thread(target=runed).start()





win.mainloop()
