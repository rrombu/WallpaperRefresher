from general import *
import sys,paperwall,wallbase

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
        if (source == '-pw') and (needwp(imgpath)): paperwall.getWOTD()
        elif (source == '-wb') and (needwp(imgpath)): wallbase.getWOTD()
    elif request == '-tag':
        if source == '-pw': paperwall.getTagged(tag)
        elif source == '-wb': wallbase.getTagged(tag)

print(' > | Screen resolution:',width,'x',height)
main()
print(' > | We are done here ')
input('\nPress Enter to exit...')