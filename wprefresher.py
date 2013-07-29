from urllib  import request
from ctypes  import *
from general import *
import os,time,sys,paperwall

img = 'wp.bmp'

def main():
    try: request = sys.argv[1]
    except IndexError: request = '-tag'
    if request == '-h':
        print('\nParameters help:\n\t-wotd - download and install Wallpaper of the Day\n\t-tag [TEXT] - downloads and install tagged wallpaper\n')
    elif request == '-wotd':
        paperwall.needwp(imgpath)
        setwp(imgpath)
    elif request == '-tag':
        tag = ''
        for i in range(2,len(sys.argv)):
            tag += sys.argv[i]+' '
        paperwall.getTagged(tag)

print(' > | Screen resolution:',width,'x',height)
main()
print(' > | We are done here ')
input('\nPress Enter to exit...')
