#!coding=utf-8
import sys, os, time
import urllib2
import urllib
import json
import traceback
import  random
from bs4 import BeautifulSoup
import re
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


class MusicInfo:

  def __init__(self):
    self.singer  = ''
    self.title   = ''
    self.mhash   = ''
    self.tlen    = 0
    self.albumid = 0
    self.fsize   = 0
    self.url     = ''
    self.path    = ''
    self.upurl   = ''

  def Show(self):
    print "singer: %s title: %s hast: %s timelen: %s album: %s filesize: %s url: %s upurl: %s" % (self.singer.decode('utf-8'), self.title.decode('utf-8'), self.mhash, str(self.tlen), self.albumid, str(self.fsize), self.url, self.upurl)

  def Save(self, fstream):
    fstream.write(self.singer.decode('utf-8') + '\n')
    fstream.write(self.title.decode('utf-8') + '\n')
    fstream.write(self.mhash + '\n')
    fstream.write(str(self.tlen) + '\n')
    fstream.write(str(self.albumid) + '\n')
    fstream.write(str(self.fsize) + '\n')
    fstream.write(str(self.url) + '\n')
    fstream.write(self.path + '\n')
    fstream.write(self.upurl + '\n')

def HttpRequest(url):
  userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "  
  headers = { 'User-Agent' : userAgent }

  req = urllib2.Request(url, headers = headers)
  response = urllib2.urlopen(req)
  the_page = response.read()
  code = response.getcode()
  #print code
  if(code != 200):
    print code, url
  #print the_page
  return  the_page

def GetMusicPlayURL(music_hash, album_id):
  ts = int(time.time())
  ts = ts * 1000 + 80
  # http://www.kugou.com/yy/index.php?r=play/getdata&hash=3C3D93A5615FB42486CAB22024945264&album_id=1645030&_=1499661154591
  url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash="
  url = url + music_hash + "&album_id=" + str(album_id) + "&_=" + str(ts)
  content = HttpRequest(url)
  jdata = json.loads(content)
  play_url = jdata['data']["play_url"]
  return play_url

def GetMusicInfos(content):
  soup = BeautifulSoup(content, "html.parser")
  singers = []
  musics  = []
  for a in soup.find_all('li'):
    if(a.has_attr('data-index')):
      title = a['title'].encode('utf-8')
      # format: singer - music_name
      texts = title.split(' - ')
      #print texts[0].decode('utf-8')
      #print texts[1].decode('utf-8')
      singers.append(texts[0])
      musics.append(texts[1])
  # get hash data
  data = re.search('global.features = \[\{.*?\}\];', content)
  jvar = data.group(0)
  pos = jvar.find('=')
  pos += 1
  jdata = jvar[pos:-1]
  #print jdata
  jtext = json.loads(jdata)
  music_hashs = []
  time_lens   = []
  album_ids   = []
  file_sizes  = []
  for music in jtext:
    music_hashs.append(music['Hash'])
    time_lens.append(music['timeLen'])
    album_ids.append(music['album_id'])
    file_sizes.append(music['size'])

  music_list = []
  for idx in range(len(music_hashs)):
    play_url = GetMusicPlayURL(music_hashs[idx], album_ids[idx])
    m = MusicInfo()
    m.singer = singers[idx]
    m.title  = musics[idx]
    m.mhash = music_hashs[idx]
    m.tlen  = time_lens[idx]
    m.albumid = album_ids[idx]
    m.fsize   = file_sizes[idx]
    m.url     = play_url
    music_list.append(m)

  return music_list

def Download(m):
  pos = m.url.rfind('/')
  pos = pos + 1
  filename = m.url[pos:]
  filename = './data/'+ filename
  m.path = filename 
  print "down %s ==> %s" % (m.url, filename)
  print urllib.urlretrieve(m.url, filename)

def GetTop500Page(idx, fstream):
  url = "http://www.kugou.com/yy/rank/home/"
  url = url + str(idx) + "-8888.html?from=rank"
  content = HttpRequest(url)
  music_list = GetMusicInfos(content)
  for m in music_list:
    Download(m)
    m.Save(fstream)


if __name__ == '__main__':
  fstream = open("source.info", "wb")
  for idx in xrange(1,23):
    GetTop500Page(idx, fstream)
  #GetTop500Page(1, fstream)
