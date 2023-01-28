import json
import os
import web

def getmainversion(ids:str|None=None):
	with open('version_manifest.json') as f:
		versions=json.load(f)
	if ids:
		v=ids
	else:
		latest=versions.get('latest')
		v=latest.get('release')
	vs=versions.get('versions')
	ver=dict()
	for a in vs:
		if v==a.get('id'):
			ver=a
	if not ver:
		raise Exception
	vers=ver.get('id')
	verpath=os.path.join('.minecraft','versions',vers,vers+'.json')
	web.download(ver.get('url'),verpath,isjson=True)
	return verpath
if __name__=='__main__':
	getmainversion('rd-132211')