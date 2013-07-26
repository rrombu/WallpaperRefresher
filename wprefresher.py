from urllib import request
from bs4    import BeautifulSoup
from ctypes import *
import os,time

img = 'wp.bmp'
imgpath = os.path.abspath(img)

def needwp(img):
    modified = time.ctime(os.stat(img).st_mtime)
    modified = modified.split()
    modified = modified[2]
    print('Wp modified: '+modified)
    today = time.strftime('%d')
    if modified!=today:
        print('Wallpaper needs update!')
        return True
    else:
        print('Wallpaper is up to date.')
        return False
    

def setwp(img):
    ''' (string)
    Set's wallpaper in Windows to an bmp file, specified in parameter.
    '''
    print(' > Setting up new wallpaper...')
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE   = 0x1
    path = bytes(img, 'utf-8')
    path = c_char_p(path)
    windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE)
    print(' + Wallpaper SET!')

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    if s[1]=='i':
        begin = s.find('wallp')
        end = s.find('jpg')+3
        link = s[begin:end]
    elif s[1]=='d':
        begin = s.find('wallp')
        end = s.find('target',begin)-2
        link = s[begin:end]
    result = 'http://thepaperwall.com/' + link
    return result

def getWOTD(img):
    ''' (string)
    Finds and downloads Wallpaper of the Day at paperwall.com for further use.
    '''
    print(' > Downloading image...')
    page = request.urlopen('http://thepaperwall.com/index.php')
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='active'))
    link = getLink(block)

    page = request.urlopen(link)
    soup = BeautifulSoup(page)
    block = str(soup.find('img',class_='wall_img'))
    link = getLink(block)

    picture = request.urlopen(link)
    print(' > Saving image...')
    CHUNK = 16 * 1024
    with open(img,'wb') as f:
        while True:
            chunk = picture.read(CHUNK)
            if not chunk: break
            f.write(chunk)
    print(' + Image obtained')

# Main body
if needwp(imgpath):
    getWOTD(imgpath)
    setwp(imgpath)

print('\n=== We are done here ===')
