from urllib  import request
from bs4     import BeautifulSoup
from general import *
from PyQt4   import QtGui, QtCore
QString = type("")

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    if s[1]=='i':
        begin = s.find('src')+5
        end = s.find('">')
        return s[begin:end]
    elif s[1]=='a':
        begin = s.find('http')
        end = s.find('"',begin)
        return s[begin:end]
    elif s[1]=='d':
        begin = s.find('id="thumb')+9
        end = s.find('" ',begin)
        result = 'http://wallbase.cc/wallpaper/' + s[begin:end]
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
    progress.setWindowTitle('Progress')
    progress.setLabelText('Connecting to wallbase.cc ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(

    page = request.urlopen('http://wallbase.cc')
    progress.setValue(10)
    soup = BeautifulSoup(page)
    soup = soup.find_all('a',title='Featured wallpaper')
    progress.setValue(25)
    i = 0
    for wallpaper in soup:
        progress.setLabelText('Opening wallpaper page...')
        linkend = str(wallpaper).find('"',24)
        page = request.urlopen(str(wallpaper)[23:linkend])
        soup = BeautifulSoup(page)
        progress.setValue(35)
        block = str(soup.find('img',class_='wall stage1 wide'))
        link = getLink(block)
        progress.setLabelText('Downloading image...')
        progress.setValue(50)
        getImage(link)
        progress.setLabelText('Setting up wallpaper...')
        progress.setValue(90)
        setwp(imgpath)
        happiness = QtGui.QMessageBox.question(None, 'Request', 'Do you like your new wallpaper?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        i += 1
        if happiness == QtGui.QMessageBox.Yes:
            break
        elif i == 27:
            QtGui.QMessageBox.critical(None, 'Warning', 'There is no more stuff', QtGui.QMessageBox.Ok)
            break

def getTagged(tag):
    ''' (string)
    Finds, downloads and sets up wallpaper with specified tag.
    '''
    progress = QtGui.QProgressDialog(None, None, 0, 100)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    progress.setMinimum(0)
    progress.setMaximum(100)
    progress.setMinimumDuration(0)
    progress.setWindowTitle('Progress')
    progress.setLabelText('Connecting to wallbase.cc ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(
    tag2 = tag.replace(' ','%20')
    page = request.urlopen('http://wallbase.cc/search?color=&section=wallpapers&q='+tag2+'&res_opt=gteq&res='+str(width)+'x'+str(height)+'&order_mode=desc&thpp=20&purity=100&board=213&aspect=0.00')
    progress.setValue(25)
    soup = BeautifulSoup(page)
    progress.setLabelText('Searching: '+tag)
    group = soup.find_all('a',target="_blank")
    for i in range(len(group)-1,len(group)-5,-1):  # Filters social buttons
        try: group.remove(group[i])
        except IndexError: break

    for s in group:
        group[group.index(s)] = getLink(str(s))

    n = 0
    while True:
        progress.setValue(50)
        try: page = request.urlopen(group[n])
        except IndexError:
            if n>0:
                QtGui.QMessageBox.critical(None, "Warning", 'There is no more stuff', QtGui.QMessageBox.Ok)
                break
            else:
                QtGui.QMessageBox.critical(None, "Warning", 'Found nothing! Check or change your request.', QtGui.QMessageBox.Ok)
                break
        soup = BeautifulSoup(page)
        block = str(soup.find('img',class_='wall stage1 wide'))
        link = getLink(block)
        progress.setLabelText('Downloading image...')
        progress.setValue(50)
        getImage(link)
        progress.setLabelText('Setting up wallpaper...')
        progress.setValue(90)
        setwp(imgpath)
        happiness = QtGui.QMessageBox.question(None, 'Request', 'Do you like your new wallpaper?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if happiness == QtGui.QMessageBox.Yes:
            break
        else: n+=1