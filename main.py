from urllib3.exceptions import HTTPError
import tkinter as tk
import requests
import tkinter.messagebox
from tkinter import ttk
import json
import getauthlib_injector
import getindex
import getlib
import getmainversion
import getmainjar
import os
import web
import launch
import threading
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
}
root = tk.Tk()
root.geometry('600x600')
root.title("Python Minecraft Launcher")


def getobject(assetsPath: str):
    rootweb = 'https://resources.download.minecraft.net/'
    objpath = os.path.join('.minecraft', 'assets', 'objects')
    with open(assetsPath) as f:
        assets = json.load(f)
    objects = assets.get('objects')
    objhashlist = list()
    twoobjhashlist = list()
    objsizelist = list()
    for a in objects.values():
        objhashlist.append(a.get('hash'))
        twoobjhashlist.append(a.get('hash')[:2])
        objsizelist.append(a.get('size'))
    urlobjdict = dict()
    for b in zip(twoobjhashlist, objhashlist):
        urlobjdict[os.path.join(objpath, b[0], b[1])] = [
            rootweb+b[0]+'/'+b[1], b[1]]
    errors = list()
    for p, things in urlobjdict.items():
        u: str = things[0]
        h = things[1]
        try:
            web.download(u, p, 'sha1', h)
            print(h)
        except KeyboardInterrupt:
            break
        except:
            try:
                u = u.replace('https://resources.download.minecraft.net/',
                              'https://bmclapi2.bangbang93.com/assets/')
                web.download(u, p, 'sha1', h)
            except (requests.exceptions.ConnectionError, HTTPError):
                u = u.replace('https://bmclapi2.bangbang93.com/assets/',
                              'https://download.mcbbs.net/assets/')
                web.download(u, p, 'sha1', h)
    err1 = list()
    if len(errors) != 0:
        for a in errors:
            u = a[0]
            h = a[1]
            try:
                web.download(u, p, 'sha1', h)
            except KeyboardInterrupt:
                break
            except:
                err1.append(a)
        if err1 != []:
            print(err1)
        else:
            tkinter.messagebox.showinfo('info','资源下载完成')
        return
    tkinter.messagebox.showinfo('info','资源下载完成')


def getlib(mainversionpath: str):
    mainversionpath=os.path.abspath(mainversionpath)
    gamedir=os.path.split(os.path.split(os.path.split(os.path.abspath(mainversionpath))[0])[0])[0]
    hasnatives=False
    with open(mainversionpath) as f:
        things: dict = json.load(f)
    librariesPath = os.path.abspath(os.path.join('.minecraft', 'libraries'))
    libs: list = things.get('libraries')
    libdict = dict()
    for t in libs:
        t1: dict = t.get('downloads').get('artifact')
        if t.get('downloads').get('classifiers')!=None:
            hasnatives=True
        if t1==None:
            continue
        rules = t.get('rules')
        if rules != None and len(rules) == 1:
            rules = rules[0]
            oses = rules.get('os')
            if oses != None:
                osname = oses.get('name')
                if osname != None:
                    if osname != 'windows':
                        continue
        p = os.path.join(librariesPath, (t1.get('path')).replace('/', '\\'))
        libdict[t1.get('sha1')] = [p, t1.get('url')]
    del p, t
    cp = '"'
    error = dict()
    for h, pu in libdict.items():
        p = pu[0]
        u: str = pu[1]
        try:
            web.download(u, p, 'sha1', h)
        except (requests.exceptions.ConnectionError, HTTPError):
            try:
                u = u.replace('https://libraries.minecraft.net/',
                              'https://bmclapi2.bangbang93.com/maven/')
                web.download(u, p, 'sha1', h)
            except (requests.exceptions.ConnectionError, HTTPError):
                u = u.replace('https://bmclapi2.bangbang93.com/maven/',
                              'https://download.mcbbs.net/maven/')
                web.download(u, p, 'sha1', h)
        print(p)
        cp += p+';'
    if hasnatives:
        import getnatives
        getnatives.getnatives(mainversionpath,os.path.join(os.path.split(mainversionpath)[0],'natives'))
    tkinter.messagebox.showinfo(message=f'库下载完成，cp: {cp}')
    mainversionpath = os.path.abspath(mainversionpath)
    cp = cp+os.path.split(mainversionpath)[0] + '\\' +\
        os.path.split(mainversionpath)[1].rstrip('.json')+'.jar'
    if not cp.endswith('"'):
        cp=cp+'"'
    with open('cp.txt', 'w') as f:
        f.write(cp)


def download():
    mainverpath = getmainversion.getmainversion(verchoose.get())
    indexpath = getindex.getindex(mainverpath)
    t = threading.Thread(target=getobject, args=(indexpath,))
    t.start()
    t1 = threading.Thread(target=getlib, args=(mainverpath,))
    t1.start()
    t2 = threading.Thread(target=getmainjar.getmainjar, args=(mainverpath,))
    t2.start()
    t3 = threading.Thread(
        target=getauthlib_injector.getauthlib_injector, args=tuple())
    t3.start()


def littleskinlogin():
    import littleskinUUID
    userinfo = {"agent": {
        "name": "Minecraft",
                "version": 1
    },
        "username": littleskinusernameEntry.get(),
        "password": littleskinpasswordEntry.get(),
        "requestUser": False,
        "clientToken": "ssssdddadfsdfsfsffsxxdsfewfsdf",
        "token": None}
    user = littleskinUUID.littleskinUUID(userinfo)
    with open('littleskinGet.json', 'w') as f:
        json.dump(user, f)
    tkinter.messagebox.showinfo('info','登录成功')
verchoose=tk.StringVar()
veroption=list()
downloadFrame=tk.Frame(root)
hasverlist=False

def refresh():
    global verchoose,veroption,hasverlist,verlist
    if hasverlist:
        verlist.pack_forget()
    try:
        os.remove('version_manifest.json')
    except:
        pass
    try:
        r = requests.get(
            'https://piston-meta.mojang.com/mc/game/version_manifest.json', headers=header)
    except (requests.exceptions.ConnectionError, HTTPError):
        try:
            r = requests.get(
                'https://bmclapi2.bangbang93.com/mc/game/version_manifest.json', headers=header)
        except (requests.exceptions.ConnectionError, HTTPError):
            r = requests.get(
                'https://download.mcbbs.net/mc/game/version_manifest.json', headers=header)
    j: dict = json.loads(r.text)
    r.close()
    with open('version_manifest.json', 'w') as f:
        json.dump(j, f, indent=4)
    version = j
    allversion = version.get('versions')
    veroption = list()
    for verdict in allversion:
        if str(verdict.get('type')).startswith('old'):
            continue
        veroption.append(verdict.get('id'))
    verchoose = tk.StringVar()
    verchoose.set(veroption[0])
    verlist = ttk.Combobox(downloadFrame, state='normal',
                        textvariable=verchoose, values=veroption)
    verlist.pack()
    hasverlist=True
downloadbtn = tk.Button(downloadFrame, text='下载', command=download)
littleskinusernameEntry: tk.Entry
littleskinpasswordEntry: tk.Entry
playeroptions=tk.StringVar()

def launcher():
    l=tk.Toplevel(root)
    with open('littleskinGet.json') as f:
        userinfo=json.load(f)
    players=userinfo.get('availableProfiles')
    playeroptions=tk.StringVar()
    playerlist=list()
    for player in players:
        playerlist.append(player.get('name'))
    def mainlaunch():
        old=False
        player=playeroptions.get()
        with open('launcher_profiles.json') as f:
            profile=json.load(f)
        profiles=profile.get('profiles')
        gamedir=profiles.get('gameDir')+'\\'
        javapathes:dict=profile.get('JavaPath')
        mainverpath=gamedir+'versions\\'+verchoose.get()+'\\'+verchoose.get()+'.json'
        with open(mainverpath) as f:
            mainver:dict=json.load(f)
        with open('cp.txt') as f:
            cp=f.read()
        with open('littleskinGet.json') as f:
            userinfo=json.load(f)
        javaversion=str(mainver.get('javaVersion').get('majorVersion'))
        javapath=None
        for version,path in javapathes.items():
            if version==javaversion:
                javapath=path
        if javapath==None:
            tkinter.messagebox.showerror('Error','你没有可用的java版本')
            return
        id=str()
        accessToken=userinfo.get('accessToken')
        for i in userinfo.get('availableProfiles'):
            if i.get('name')==player:
                id=i.get('id')
        if 'minecraftArguments' not in mainver.keys():
            launch.launch(mainverpath,cp,player,id,accessToken,gamedir+'assets',javapath,profiles.get('gameDir'),'javaangent.txt','MjM2MmE', '2535423162686803','Mojang',os.path.join(os.path.split(mainverpath)[0],'natives'))
        else:
            old=True
            launch.launchold(mainverpath,cp,player,id,profiles.get('gameDir'),gamedir+'assets',javapath,gamedir+'versions\\'+verchoose.get()+'natives')
        b=tkinter.messagebox.askyesno(message='启动脚本已生成，是否启动')
        if b:
            if old:
                os.system('start_old.bat')
            else:
                os.system('start.bat') 
    ttk.Combobox(l, state='normal',
                        textvariable=playeroptions, values=playerlist).pack()
    tk.Button(l,text='确定',command=mainlaunch).pack()

def littleskin():
    global littleskinusernameEntry, littleskinpasswordEntry
    try:
        os.remove("littleskinGet.json")
    except FileNotFoundError:
        pass
    try:
        os.remove('littleskinPosts.json')
    except FileNotFoundError:
        pass
    l = tk.Toplevel(root)
    l.title('littleskinLogin')
    l.geometry('300x300')
    emailFrame = tk.Frame(l)
    tk.Label(emailFrame, text='littleskin邮箱: ').pack(fill=tk.Y)
    littleskinusernameEntry = tk.Entry(emailFrame)
    littleskinusernameEntry.pack(fill=tk.Y)
    emailFrame.pack()
    pwdFrame = tk.Frame(l)
    tk.Label(pwdFrame, text='littleskin密码: ').pack(fill=tk.Y)
    littleskinpasswordEntry = tk.Entry(pwdFrame, show='*')
    littleskinpasswordEntry.pack(fill=tk.Y)
    pwdFrame.pack()
    loginbtn = tk.Button(l, text='登录', command=littleskinlogin)
    loginbtn.pack()
tk.Button(downloadFrame, text='刷新列表', command=refresh).pack()
downloadbtn.pack()
downloadFrame.pack()
tk.Button(root, text='littleskin登录', command=littleskin).pack()
tk.Button(root, text='启动', command=launcher).pack()
root.mainloop()
