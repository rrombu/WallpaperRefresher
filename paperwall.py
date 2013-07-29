from urllib  import request
from bs4     import BeautifulSoup
from ctypes  import *
from general import *
import os,time,sys

def needwp(img):
    ''' (string) -> boolean
    Checks if wallpaper image needs update by watching date of bmp modification
    '''
    modified = time.ctime(os.stat(img).st_mtime)
    modified = modified.split()
    modified = modified[2]
    print(' > | Wp modified: '+modified)
    today = time.strftime('%d')
    if modified!=today:
        print(' ! | Wallpaper needs update!')
        getWOTD()
    else:
        print(' + | Wallpaper is up to date.')

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    if s[1]=='i':
        begin = s.find('wallp')
        end = max(s.find('jpg'), s.find('png'))+3
        link = s[begin:end]
    elif s[1]=='d':
        begin = s.find('wallp')
        end = s.find('" ',begin)
        link = s[begin:end]
    result = 'http://thepaperwall.com/' + link
    return result

def getWOTD():
    ''' 
    Finds and downloads Wallpaper of the Day at paperwall.com for further use.
    '''
    print(' > | Getting you Wallpaper of the day...')
    page = request.urlopen('http://thepaperwall.com/index.php')
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='active'))
    link = getLink(block)

    page = request.urlopen(link)
    soup = BeautifulSoup(page)
    block = str(soup.find('img',class_='wall_img'))
    link = getLink(block)
    getImage(link)

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''    
    print(' > | You are looking for wallpaper tagged: '+tag)
    tag = tag.replace(' ','+')
    tag = tag[:len(tag)-1]
    page = request.urlopen('http://thepaperwall.com/search.php?search='+tag)
    soup = BeautifulSoup(page)
    group = soup.find_all('div',class_='single_thumbnail_cont')

    # First filter: resolution
    for s in group:
        sstr = str(s)
        begin = sstr.find('<span>')+6
        end = sstr.find('</span>')
        resol = sstr[begin:end].split()
        resol.remove('x')
        if int(resol[0])<width or int(resol[1])<height:
            group.remove(s)

    # Second filter: clean links
    for s in group:
        group[group.index(s)] = getLink(str(s))

    n = 0
    while True:
        try: page = request.urlopen(group[n])
        except IndexError:
            if n>0:
                print(' ! | I got nothing more :( ')
                break
            else:
                print(' ! | I found nothing :( ')
                break
        soup = BeautifulSoup(page)
        block = str(soup.find('img',class_='wall_img'))
        link = getLink(block)
        getImage(link)
        setwp(imgpath)
        if input(' ? | You happy now? (y/n) ')=='y': break
        else: n+=1
