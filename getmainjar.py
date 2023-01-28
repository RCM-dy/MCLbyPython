import json
import os
import web


class ModeNotFoundError(KeyError):
    pass


def getmainjar(mainversionpath, mode: str | None = None):
    if mode == None:
        mode = 'client'
    if mode not in ('client', 'server'):
        raise ModeNotFoundError(f'can\'t found {mode} mode')
    path = os.path.split(mainversionpath)[0]
    with open(mainversionpath) as f:
        things = json.load(f)
    jar = things.get('downloads')
    thing: dict = jar.get(mode)
    thing_mappings: dict = jar.get(mode+'_mappings')
    try:
        web.download(thing.get('url'), os.path.join(
            path, things.get('id')+'.jar'), 'sha1', thing.get('sha1'))
    except KeyboardInterrupt:
        pass
    except:
        web.download(thing_mappings.get('url'), os.path.join(
            path, things.get('id')+'.jar'), 'sha1', thing_mappings.get('sha1'))
if __name__=="__main__":
    getmainjar(r'C:\Users\Fish Dai\Desktop\MCL\.minecraft\versions\rd-132211\rd-132211.json')