from general import *
import sys,paperwall,wallbase
from PyQt4 import QtCore, QtGui

img = 'wp.bmp'
source = ''
mode = 'wotd'

class UI(QtGui.QWidget):
    def __init__(self,*args):
        QtGui.QWidget.__init__(self,*args)
        self.setWindowTitle(u"WR")

        button = QtGui.QPushButton("BRING IT ON!")

        srcbox = QtGui.QComboBox()
        srcbox.addItem(u"Choose source")
        srcbox.addItem("Wallbase")
        srcbox.addItem("Paperwall")

        request = QtGui.QGroupBox(u"Choose mode")
        request_lay = QtGui.QVBoxLayout(request)
        request1 = QtGui.QRadioButton(u"Get me most precious one today!", request)
        request2 = QtGui.QRadioButton(u"I don't like to live dangerously.\nFind me on of these...", request)
        request1.setChecked(True)
        request_lay.addWidget(request1)
        request_lay.addWidget(request2)

        self.search = QtGui.QLineEdit()
        self.search.hide()

        self.connect(button, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(srcbox, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_source)
        self.connect(request1, QtCore.SIGNAL("toggled(bool)"),self.change_mode)
        self.connect(request2, QtCore.SIGNAL("toggled(bool)"),self.search.setVisible)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(srcbox)
        layout.addWidget(request)
        layout.addWidget(self.search)
        layout.addWidget(button)
        self.setLayout(layout)
    def change_source(self,i):
        global source
        if i == 1: source = 'wallbase'
        elif i == 2: source = 'paperwall'
        print('Source changed to',source)
    def change_mode(self,t):
        global mode
        if t: mode = 'wotd'
        else: mode = 'tag'
        print('Request changed to',mode)
    def run(self):
        request = self.search.text()
        if source == 'wallbase':
            if mode == 'wotd' and needwp(imgpath):
                wallbase.getWOTD()
            elif mode == 'tag': wallbase.getTagged(request)
        elif source == 'paperwall':
            if mode == 'wotd' and needwp(imgpath):
                paperwall.getWOTD()
            elif mode == 'tag': paperwall.getTagged(request)

app = QtGui.QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec_())