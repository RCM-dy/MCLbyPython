import requests
import json
import hashlib
import os
import base64
def getauthlib_injector(build_number:str|None=None):
	with open('headers.json') as f:
		header=json.load(f)
	try:
		r=requests.get('https://authlib-injector.yushi.moe/artifacts.json',headers=header)
		j=json.loads(r.text)
		r.close()
		with open('authlib_injector.json','w') as f:
			json.dump(j,f,indent=4)
		if build_number==None:
			r=requests.get('https://authlib-injector.yushi.moe/artifact/latest.json',headers=header)
			js:dict=json.loads(r.text)
			build_number=js.get('build_number')
			with open(f'{build_number}.json','w') as f:
				json.dump(js,f,indent=4)
		else:
			r=requests.get(f'https://authlib-injector.yushi.moe/artifact/{build_number}.json',headers=header)
			js:dict=json.loads(r.text)
			with open(f"{build_number}.json",'w') as f:
				json.dump(js,f,indent=4)
			assert str(js.get('build_number'))==build_number
		url=js.get('download_url')
		sha256=js.get('checksums').get('sha256')
		req=requests.get(url,headers=header)
		c=req.content
		req.close()
		assert hashlib.sha256(c).hexdigest()==sha256
		with open('authlib-injector.jar','wb') as f:
			f.write(c)
	except KeyboardInterrupt:
		return
	except:
		r=requests.get('https://bmclapi2.bangbang93.com/mirrors/authlib-injector/artifacts.json',headers=header)
		j=json.loads(r.text)
		r.close()
		with open('authlib_injector.json','w') as f:
			json.dump(j,f,indent=4)
		if build_number==None:
			r=requests.get('https://bmclapi2.bangbang93.com/mirrors/authlib-injector/artifact/latest.json',headers=header)
			js:dict=json.loads(r.text)
			build_number=js.get('build_number')
			with open(f'{build_number}.json','w') as f:
				json.dump(js,f,indent=4)
		else:
			r=requests.get(f'https://bmclapi2.bangbang93.com/mirrors/authlib-injector/artifact/{build_number}.json',headers=header)
			js:dict=json.loads(r.text)
			with open(f"{build_number}.json",'w') as f:
				json.dump(js,f,indent=4)
			assert str(js.get('build_number'))==build_number
		url=js.get('download_url')
		sha256=js.get('checksums').get('sha256')
		req=requests.get(url,headers=header)
		c=req.content
		req.close()
		assert hashlib.sha256(c).hexdigest()==sha256
		with open('authlib-injector.jar','wb') as f:
			f.write(c)
	os.remove(f"{build_number}.json")
	os.remove('authlib_injector.json')
	r=requests.get('https://littleskin.cn/api/yggdrasil',headers=header)
	javaagent=f'-javaagent:"{os.path.abspath("authlib-injector.jar")}"=https://littleskin.cn/api/yggdrasil'
	Dauthlibinjector_yggdrasil_prefetched=javaagent+' -Dauthlibinjector.yggdrasil.prefetched='+base64.b64encode(r.text.encode()).decode()
	with open('javaangent.txt','w') as f:
		f.write(Dauthlibinjector_yggdrasil_prefetched)
if __name__=='__main__':
	getauthlib_injector()
