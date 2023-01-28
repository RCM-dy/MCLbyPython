import json
import c
import os
import web


def getindex(path):
    ver = str(os.path.split(path)[1]).rstrip('.json')
    assetsPath = os.path.join(os.curdir, '.minecraft', 'assets', 'indexes')
    with open(path) as f:
        v: dict = json.load(f)
    assets = v.get('assetIndex')
    assetsIndex = c.assets(assets)
    assertJsonPath = os.path.join(assetsPath, assetsIndex.id+'.json')
    web.download(assetsIndex.url, assertJsonPath,
                 'sha1', assetsIndex.sha1, isjson=True)
    return assertJsonPath
if __name__=='__main__':
    getindex(r'C:\Users\Fish Dai\Desktop\MCL\.minecraft\versions\rd-132211\rd-132211.json')