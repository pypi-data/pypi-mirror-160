import os
import urllib.parse as urlparse
import time 
import requests

def download_file(url, dest):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

def Wget(url:str, dest:str=None, override=True):
    if dest == None:
        fname = os.path.basename(urlparse.urlparse(url).path)
        if len(fname.strip(" \n\t.")) == 0:
            dest = "wget.downloaded." + str(time.time())
        else:
            dest = fname

    if os.path.exists(dest):
        if override:
            download_file(url, dest)
        else:
            raise Exception(f"目标文件已存在: {dest}")
    else:
        download_file(url, dest)
    