from urllib import request
from ctypes import *
import os,sys

width = windll.user32.GetSystemMetrics(0)
height = windll.user32.GetSystemMetrics(1)
img = 'wp.bmp'
imgpath = os.path.abspath(img)

def setwp(img):
    ''' (string)
    Set's wallpaper in Windows to an bmp file, specified in parameter.
    '''
    print(' > | Setting up new wallpaper...')
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE   = 0x1
    path = bytes(img, 'utf-8')
    path = c_char_p(path)
    windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE)
    print(' + | Wallpaper SET!')

def getImage(url):
    ''' (string)
    Downloads and saves image with url
    '''
    picture = request.urlopen(url)
    print(' > | Saving image...')
    CHUNK = 16 * 1024
    with open(img,'wb') as f:
        while True:
            chunk = picture.read(CHUNK)
            if not chunk: break
            f.write(chunk)
    print(' + | Image obtained') 
