from urllib  import request
from bs4     import BeautifulSoup
from general import *
from PyQt4   import QtGui, QtCore

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
    progress = QtGui.QProgressDialog(None, None, 0, 100)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimum(0)
    progress.setMaximum(100)
    progress.setMinimumDuration(0)
    progress.setWindowTitle('Let me see...')
    progress.setLabelText('Connecting to thepaperwall.com ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(

    page = request.urlopen('http://thepaperwall.com/index.php')
    progress.setValue(10)
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='active'))
    link = getLink(block)
    progress.setValue(25)

    progress.setLabelText('Opening wallpaper page...')
    page = request.urlopen(link)
    progress.setValue(35)
    soup = BeautifulSoup(page)
    block = str(soup.find('img',class_='wall_img'))
    link = getLink(block)
    progress.setLabelText('Downloading image...')
    progress.setValue(50)
    getImage(link)
    progress.setLabelText('Setting up wallpaper...')
    progress.setValue(90)
    setwp(imgpath)

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''
    progress = QtGui.QProgressDialog(None, None, 0, 100)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimum(0)
    progress.setMaximum(100)
    progress.setMinimumDuration(0)
    progress.setWindowTitle('Let me see...')
    progress.setLabelText('Connecting to thepaperwall.com ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(

    raw_tag = tag
    tag = tag.replace(' ','+')
    tag = tag[:len(tag)]
    page = request.urlopen('http://thepaperwall.com/search.php?search='+tag)
    progress.setValue(15)
    soup = BeautifulSoup(page)
    progress.setLabelText('Getting you some '+raw_tag)
    group = soup.find_all('div',class_='single_thumbnail_cont')
    progress.setValue(25)

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
        progress.setValue(50)
        try: page = request.urlopen(group[n])
        except IndexError:
            if n>0:
                QtGui.QMessageBox.critical(None, "I'm so sorry!", 'I got nothing more :(', QtGui.QMessageBox.Ok)
                break
            else:
                QtGui.QMessageBox.critical(None, "I'm so sorry!", 'I found nothing :(', QtGui.QMessageBox.Ok)
                break
        soup = BeautifulSoup(page)
        block = str(soup.find('img',class_='wall_img'))
        link = getLink(block)
        getImage(link)
        progress.setValue(90)
        setwp(imgpath)
        happiness = QtGui.QMessageBox.question(None, 'Let me ask', 'Are you happy now?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if happiness == QtGui.QMessageBox.Yes:
            break
        else: n+=1
