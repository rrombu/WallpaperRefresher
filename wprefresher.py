from urllib  import request
from ctypes  import *
from general import *
import os,time,sys,paperwall,wallbase

img = 'wp.bmp'

def main():
    try:
        source = sys.argv[1]
        request = sys.argv[2]
        if request == '-tag':
            tag = ''
            for i in range(3,len(sys.argv)):
                tag += sys.argv[i]+' '
    except IndexError: request = '-h'
    if request == '-h':
        print('\nArguments: [-SOURCE: wp, pw] [-MODE: wotd, tag [your query]]')
    elif request == '-wotd':
        if source == '-pw': paperwall.needwp(imgpath)
        elif source == '-wb': wallbase.needwp(imgpath)
    elif request == '-tag':
        if source == '-pw': paperwall.getTagged(tag)
        elif source == '-wb': wallbase.getTagged(tag)

print(' > | Screen resolution:',width,'x',height)
main()
print(' > | We are done here ')
input('\nPress Enter to exit...')
