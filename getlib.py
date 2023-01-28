import json
import os
import web
import requests
import tkinter.messagebox
from urllib.error import HTTPError


def getlib(mainversionpath:str):
    with open(mainversionpath) as f:
        things: dict = json.load(f)
    librariesPath = os.path.abspath(os.path.join('.minecraft', 'libraries'))
    libs: list = things.get('libraries')
    libdict = dict()
    for t in libs:
        t1: dict = t.get('downloads').get('artifact')
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
        u = pu[1]
        try:
            web.download(u, p, 'sha1', h)
            print(p)
            cp += p+';'
        except KeyboardInterrupt:
            return
        except:
            error[h] = pu
    if len(error.keys())==0:
        cp = cp+os.path.split(mainversionpath)[0] + '\\' +\
        os.path.split(mainversionpath)[1].rstrip('.json')+'.jar'+'"'
        with open('cp.txt', 'w') as f:
            f.write(cp.rstrip(';')+'"')
    else:
        print(error)
if __name__=='__main__':
    getlib(r'C:\Users\Fish Dai\Desktop\MCL\.minecraft\versions\1.13\1.13.json')