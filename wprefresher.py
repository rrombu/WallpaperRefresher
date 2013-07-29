from urllib import request
from bs4    import BeautifulSoup
from ctypes import *
import os,time,sys

width = windll.user32.GetSystemMetrics(0)
height = windll.user32.GetSystemMetrics(1)

img = 'wp.bmp'
imgpath = os.path.abspath(img)

def needwp(img):
    ''' (string) -> boolean
    Checks if wallpaper image needs update by watching date of bmp modification
    '''
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
        end = max(s.find('jpg'), s.find('png'))+3
        link = s[begin:end]
    elif s[1]=='d':
        begin = s.find('wallp')
        end = s.find('" ',begin)
        link = s[begin:end]
    result = 'http://thepaperwall.com/' + link
    return result

def getImage(url):
    ''' (string)
    Downloads and saves image with url
    '''
    picture = request.urlopen(url)
    print(' > Saving image...')
    CHUNK = 16 * 1024
    with open(img,'wb') as f:
        while True:
            chunk = picture.read(CHUNK)
            if not chunk: break
            f.write(chunk)
    print(' + Image obtained')    

def getWOTD():
    ''' 
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

    getImage(link)

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''    
    print('Wallpaper tagged: '+tag)
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
    while n!=10:
        page = request.urlopen(group[n])
        soup = BeautifulSoup(page)
        block = str(soup.find('img',class_='wall_img'))
        link = getLink(block)
        getImage(link)
        setwp(imgpath)
        if input('You happy now? (y/n) ')=='y': break
        else: n+=1

def main():
    try: request = sys.argv[1]
    except IndexError: request = '-h'
    if request == '-h':
        print('\nParameters help:\n\t-wotd - download and install Wallpaper of the Day\n\t-tag [TEXT] - downloads and install tagged wallpaper\n')
    elif request == '-wotd':
        if not needwp(imgpath):
            getWOTD()
            setwp(imgpath)        
    elif request == '-tag':
        tag = sys.argv[2]
        getTagged(tag)

# Main body
print('Screen resolution:',width,'x',height)
main()
print('\n=== We are done here ===')
