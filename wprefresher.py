#!python

from ctypes import *
from os import path

SPI_SETDESKWALLPAPER = 0x14
SPIF_UPDATEINIFILE   = 0x1

img = c_char_p(b'C:\\Users\\Roman\\Documents\\GitHub\\WallpaperRefresher')

SystemParametersInfo = windll.user32.SystemParametersInfoA

print(SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, img, SPIF_UPDATEINIFILE))
