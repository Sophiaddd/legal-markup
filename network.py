import urllib.request
import xml.etree.ElementTree
import base64
import os

xmlns={ 'atom' : '{http://www.w3.org/2005/Atom}' }

def url_encode(url):
    burl=base64.urlsafe_b64encode(url.encode('utf-8')).decode('utf-8')
    return burl

def cache_get(url, dir="downloads"):
    burl=url_encode(url)
    if not os.path.exists(dir):
        os.makedirs(dir) # very obscure race condition possible leading to OSError
    bfile=os.path.join(dir, burl)
    if os.path.exists(bfile):
        print("Reading from file {0}".format(bfile))
        bstream=open(bfile, 'r', encoding="utf-8")
        html=bstream.read()
        print("Read {0} bytes".format(len(html)))
        bstream.close()
    else:
        print("Downloading url {0} to file {1}".format(url, bfile))
        response=urllib.request.urlopen(url)
        html=response.read().decode('utf-8') # Warning! Assues utf-8 encoding
        bstream=open(bfile, 'w', encoding="utf-8")
        bstream.write(html)
        bstream.close()
    return html


def get(url, dir='downloads', force=False):
    #reader=urllib.request.urlopen(url)
    #result=reader.read()
    result=cache_get(url, dir)

    return result

def atom_feed(url):
    s=get(url)
    e=xml.etree.ElementTree.fromstring(s)
    yield(e)
    #rel_link=e.findall('{atom}link'.format(**xmlns))
    next_link=e.findall("{atom}link[@rel='next']".format(**xmlns))
    while len(next_link) > 0:
        url=next_link[0].attrib['href']
        s=cache_get(url)
        e=xml.etree.ElementTree.fromstring(s)
        yield e
        next_link=e.findall("{atom}link[@rel='next']".format(**xmlns))
    
def atom_feed_single(url):
    s=get(url)
    e=xml.etree.ElementTree.fromstring(s)
    return e
