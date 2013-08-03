from urllib  import request
from urllib  import parse
from bs4     import BeautifulSoup
from general import *
from PyQt4   import QtGui, QtCore
import base64
QString = type("")

def getLink(s):
    ''' (string) -> string
    Cuts necessary link from part of the html page.
    '''
    result = 'None'
    if s[1]=='s':
        begin = s.find('+B')+4
        end = s.find(')+')-1
        result = str(base64.b64decode(s[begin:end]),encoding='UTF-8')
    elif s[1]=='d':
        begin = s.find('id="thumb')+9
        end = s.find('" ',begin)
        link = s[begin:end]
        result = 'http://wallbase.cc/wallpaper/' + link
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
    progress.setLabelText('Connecting to wallbase.cc ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(

    page = request.urlopen('http://wallbase.cc/toplist/0/12/gteq/'+str(width)+'x'+str(height)+'/0/100/32/1d')
    progress.setValue(10)
    soup = BeautifulSoup(page)
    block = str(soup.find('div',class_='thumb'))
    link = getLink(block)
    progress.setValue(25)

    progress.setLabelText('Opening wallpaper page...')
    page = request.urlopen(link)
    progress.setValue(35)
    soup = BeautifulSoup(page)
    soup = soup.find_all('div',class_='right')
    block = str(soup[len(soup)-1])
    link = getLink(block[33:])
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
    progress.setLabelText('Connecting to wallbase.cc ...')
    progress.setValue(0)    # Some crazy hack
    progress.setValue(1)    # because Progress Dialog
    progress.setValue(0)    # awakes only on third value change :(
    params = {
      'query' : tag,
      'board' : 213,    # ???
      'nsfw' : 100,     # Bit-mask: sfw-sketchy-nsfw
      'res' : str(width)+'x'+str(height), # Resolution
      'res_opt' : 'qteq',   # qteq - "at least" resolution
      'aspect' : 0,     
      'orderby' : 'random', # Change to 'random' if not testing
      'orderby_opt' : 'desc',
      'thpp' : 60,      # ???
      'section' : 'wallpapers' # ???
    }
    params = parse.urlencode(params)
    params = params.encode('utf-8')
    page = request.urlopen('http://wallbase.cc/search',params)
    progress.setValue(25)
    soup = BeautifulSoup(page)
    progress.setLabelText('Getting you some '+tag)
    group = soup.find_all('div',class_='thumb')
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
        soup = soup.find_all('div',class_='right')
        block = str(soup[len(soup)-1])
        link = getLink(block[33:])
        getImage(link)
        progress.setValue(90)
        setwp(imgpath)
        happiness = QtGui.QMessageBox.question(None, 'Let me ask', 'Are you happy now?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if happiness == QtGui.QMessageBox.Yes:
            break
        else: n+=1
