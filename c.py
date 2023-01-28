class versionses:
	def __init__(self,d:dict) -> None:
		id=d.get('id')
		type=d.get('type')
		url=d.get('url')
		time=d.get('time')
		releaseTime=d.get('releaseTime')
		self.id=id
		self.type=type
		self.url=url
		self.time=time
		self.releaseTime=releaseTime
class assets:
	def	__init__(self,d:dict) -> None:
		self.id=d.get('id')
		self.sha1=d.get('sha1')
		self.size=d.get('size')
		self.totalSize=d.get('totalSize')
		self.url=d.get('url')