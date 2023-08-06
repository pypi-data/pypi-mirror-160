import collections
import os
import requests


CachedFile = collections.namedtuple('CachedFile', 'name mtime data')

class WebFileCacheException(Exception):
    pass

class WebFileCache():
    def __init__(self, base_uri, ca=None):
        self.base_uri = base_uri
        self.ca = ca
        self.cached_files = {}

    def get(self, key):
        with requests.Session() as s:
            if self.ca is not None:
                s.verify = self.ca
            cfile = self.cached_files.get(key)
            resp = None
            if cfile is not None:
                resp = s.get(self.base_uri + key, headers = {'If-Modified-Since': cfile.mtime})
            else:
                resp = s.get(self.base_uri + key)
            if resp.status_code == 200:
                self.cached_files[key] = CachedFile(name=key, mtime=resp.headers['Last-Modified'], data=resp.content)
                return self.cached_files[key].data
            if resp.status_code == 304:  # File not modified
                return self.cached_files[key].data
            raise WebFileCacheException('File retrieval error: HTTP {resp.status_code}\n{resp.content}')

def get_public_ip():
    return requests.get(os.environ.get("PMG_IP_HOOK", "http://ifconfig.co/ip")).content.decode('utf8').strip()
