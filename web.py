import requests
import hashlib
import json
import os
edgeheader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
}


def download(url: str, path: str | None = None, hash_algorithm: str | None = None, hash: str | None = None, isjson: bool = False):
    if path == None:
        path = url.split('/')[-1]
    pathdir=os.path.split(os.path.abspath(path))[0]
    if not os.path.isdir(pathdir):
        os.makedirs(pathdir)
    r = requests.get(url, headers=edgeheader)
    c = r.content
    r.close()
    if isinstance(hash_algorithm, str) and hash_algorithm in ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                                                              'blake2b', 'blake2s',
                                                              'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                                                              'shake_128', 'shake_256'):
        match hash_algorithm:
            case 'md5':
                assert hashlib.md5(c).hexdigest() == hash
                if isjson:
                    with open(path, 'w') as f:
                        json.dump(json.loads(c),f,indent=4)
                else:
                    with open(path, 'wb') as f:
                        f.write(c)
            case 'sha256':
                assert hashlib.sha256(c).hexdigest() == hash
                if isjson:
                    with open(path, 'w') as f:
                        json.dump(json.loads(c),f,indent=4)
                else:
                    with open(path, 'wb') as f:
                        f.write(c)
            case 'sha1':
                assert hashlib.sha1(c).hexdigest() == hash
                if isjson:
                    with open(path, 'w') as f:
                        json.dump(json.loads(c),f,indent=4)
                else:
                    with open(path, 'wb') as f:
                        f.write(c)
            case 'sha224':
                assert hashlib.sha224(c).hexdigest() == hash
                if isjson:
                    with open(path, 'w') as f:
                        json.dump(json.loads(c),f,indent=4)
                else:
                    with open(path, 'wb') as f:
                        f.write(c)
    else:
        if isjson:
            with open(path, 'w') as f:
                json.dump(json.loads(c),f,indent=4)
        else:
            with open(path, 'wb') as f:
                f.write(c)
