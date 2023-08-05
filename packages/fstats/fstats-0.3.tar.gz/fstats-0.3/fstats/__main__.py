from time import sleep
from tkinter import *
import threading
import psutil
import json
import os
from importlib.machinery import SourceFileLoader


def diskStats():
    return psutil.disk_usage('/')


def cpuStats():
    return psutil.cpu_percent(interval=1)


def memStats():
    return psutil.virtual_memory().percent


def config():
    userConfigPath = os.path.join(os.environ["HOME"], ".fstats", "config.json")
    if os.path.exists(userConfigPath):
        with open(userConfigPath, 'rb') as f:
            return True, json.load(f)
    else:
        return False, None


_user, _config = config()


def get(keys, dft, conf=_config):
    if not _user:
        return dft
    if len(keys) <= 0:
        return dft
    key = keys[0]
    if key in conf.keys():
        if len(keys) == 1:
            return conf[key]
        else:
            return get(keys[1:], dft, conf[key])


def winCreate():
    win = Tk()
    win.title('fstats')
    win.configure(bg='white')
    win.overrideredirect(True)

    width = win.winfo_screenwidth()
    heigth = win.winfo_screenheight()

    win.attributes('-type', 'black')
    win.attributes('-zoomed', False)
    win.attributes('-alpha', '0.8')
    win.attributes('-topmost', True)

    userWidth = get(['width'], 96)
    userHeight = get(['height'], 48)
    win.geometry('{}x{}+{}+{}'.format(userWidth, userHeight,
                 width - userWidth - 50, heigth - userHeight - 50))
    win.resizable(width=0, height=0)

    def StartMove(event):
        win.x = event.x
        win.y = event.y

    def StopMove(event):
        win.x = None
        win.y = None

    def OnMotion(event):
        deltax = event.x - win.x
        deltay = event.y - win.y
        x = win.winfo_x() + deltax
        y = win.winfo_y() + deltay
        win.geometry("+%s+%s" % (x, y))

    win.bind("<ButtonPress-1>", StartMove)
    win.bind("<ButtonRelease-1>", StopMove)
    win.bind("<B1-Motion>", OnMotion)

    menu = Menu(win)

    def destroy():
        win.destroy()
    menu.add_command(label='退出', command=destroy)
    menu.add_command(label='取消')

    def popupmenu(event):
        menu.post(event.x_root, event.y_root)

    win.bind("<ButtonPress-3>", popupmenu)

    return win


configStyle = {
    'high': ['red', 'white'],
    'mid': ['white', 'black'],
    'low': ['white', 'black'],  # ['green', 'white'],
}


def departLevel(cpu, mem):
    if (cpu > 90 or mem > 90):
        return 'high'
    if (cpu < 20 and mem < 30):
        return 'low'
    return 'mid'


def intervalProcess(win):
    textvariable = StringVar()

    label = Label(win, justify='left', anchor='center', bg='white', fg='black', cursor='fleur',
                  font=('Monospace', 10),
                  width=win.winfo_screenwidth(), height=win.winfo_screenheight(),
                  textvariable=textvariable)
    label.pack(padx=0, pady=0)

    def refresh(textvariable):
        items = get(["items"], None)
        infoItems = []
        if items:
            for item in items:
                infoItems.append([item[0], None, item[2], SourceFileLoader(item[0], item[1]).load_module()])
        style = get(["style"], None)
        if style:
            style = SourceFileLoader('style', style).load_module()
        while True:
            info = ""
            if infoItems:
                for item in infoItems:
                    item[1] = item[-1].info()
                if style:
                    style.style(infoItems, label)
                info = '\n'.join([item[2].format(item[0], item[1]) for item in infoItems])
            else:
                cpu = cpuStats()
                mem = memStats()
                info = " {:<6}{:<5}%\n {:<5}{:<5}%".format(
                    "CPU:", cpu, "MEM:", mem)
                configLevel = configStyle[departLevel(cpu, mem)]
                label['bg'] = configLevel[0]
                label['fg'] = configLevel[1]
            textvariable.set(info)
            sleep(1)

    thread = threading.Thread(target=refresh, args=(textvariable,))
    thread.daemon = True
    thread.start()


def main():
    win = winCreate()
    intervalProcess(win)
    win.mainloop()


if __name__ == '__main__':
    main()
