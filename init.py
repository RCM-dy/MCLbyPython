import json
import os
import sys
if os.name!='nt':
    print('You are not Windows')
if sys.getwindowsversion()[0]<10:
    print('You windows is too old,you can not run these programs')
workpath = os.getcwd()
javadict=dict()
while True:
    ins=input('Input jdk path:')
    if ins=='':
        break
    if os.path.isfile(ins):
        if not ins.startswith('"'):
            ins='"'+ins
        if not ins.endswith('"'):
            ins=ins+'"'
        version=input('Input jdk version: ')
        javadict[version]=ins
gamedir = os.path.join(workpath, '.minecraft')
profiles = {'profiles':{"gameDir": gamedir, "lastVersionId": "1.14.1", "name": "(Default)"},
            "selectedProfileName": "(Default)", "JavaPath": javadict}
with open('.\\launcher_profiles.json', 'w') as f:
    json.dump(profiles, f, indent=4)
