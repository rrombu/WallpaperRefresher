from urllib import request
from ctypes import *
from PyQt4  import QtGui
import os,time

width = windll.user32.GetSystemMetrics(0)
height = windll.user32.GetSystemMetrics(1)
img = 'wp.bmp'
imgpath = os.path.abspath(img)

def setwp(img):
    ''' (string)
    Set's wallpaper in Windows to an bmp file, specified in parameter.
    '''
    SPI_SETDESKWALLPAPER = 0x14
    SPIF_UPDATEINIFILE   = 0x1
    path = bytes(img, 'utf-8')
    path = c_char_p(path)
    windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE)

def getImage(url):
    ''' (string)
    Downloads and saves image with url
    '''
    picture = request.urlopen(url)
    CHUNK = 16 * 1024
    with open(img,'wb') as f:
        while True:
            chunk = picture.read(CHUNK)
            if not chunk: break
            f.write(chunk)

def needwp(img):
    ''' (string) -> boolean
    Checks if wallpaper image needs update by watching date of bmp modification
    '''
    modified = time.ctime(os.stat(img).st_mtime)
    modified = modified.split()
    modified = int(modified[2])
    today = int(time.strftime('%d'))
    if modified!=today:
        return True
    else:
        QtGui.QMessageBox.information(None, 'Guess what?', 'Wallpaper is up to date!', QtGui.QMessageBox.Ok)
        return False
