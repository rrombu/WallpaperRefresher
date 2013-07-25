from PIL    import Image
from urllib import request
from bs4    import BeautifulSoup
from ctypes import *

# Paths to transit files
jpg_path = 'C:\\Users\\Roman\\Documents\\GitHub\\WallpaperRefresher\\wp.jpg'
bmp_path = 'C:\\Users\\Roman\\Documents\\GitHub\\WallpaperRefresher\\wp.bmp'

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

def jpg2bmp(jpg,bmp):
    ''' (string,string)
    Convert's jpg file to a bmp.
    '''
    print(' > Converting to bmp...')
    p = Image.open(jpg)
    p.save(bmp)
    print(' + Converted JPG to BMP')

def getWOTD(outjpg):
    ''' (string)
    Finds and downloads Wallpaper of the Day at paperwall.com for further use.
    '''
    print(' > Downloading image...')
    page = request.urlopen('http://thepaperwall.com/index.php')
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='active'))
    key = block[67:-200]
    link = 'http://thepaperwall.com/' + key
    print('Link to WOTD PAGE obtained: ' + link)

    page = request.urlopen(link)
    soup = BeautifulSoup(page)
    block = str(soup.find('img',class_='wall_img'))
    key = block[45:-3]
    link = 'http://thepaperwall.com' + key
    print('\nLink to WOTD JPG obtained: ' + link)

    picture = request.urlopen(link)
    CHUNK = 16 * 1024
    with open(outjpg,'wb') as f:
        while True:
            chunk = picture.read(CHUNK)
            if not chunk: break
            f.write(chunk)
    print(' + Image obtained')

# Main body
getWOTD(jpg_path)
jpg2bmp(jpg_path,bmp_path)
setwp(bmp_path)
print('\n=== We are done here ===')
