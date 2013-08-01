from general import *
import sys,paperwall,wallbase
from PyQt4 import QtCore, QtGui

img = 'wp.bmp'
source = 0

class UI(QtGui.QWidget):
    def __init__(self,*args):
        QtGui.QWidget.__init__(self,*args)
        self.setWindowTitle(u"WR")
        # создаем объекты:
        srcbox = QtGui.QComboBox()
        button = QtGui.QPushButton("Wallpaper of the Day")
        srcbox.addItem(u"Выберите источник")
        srcbox.addItem("Wallbase")
        srcbox.addItem("Paperwall")

        self.connect(button, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(srcbox, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_source)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(srcbox)
        layout.addWidget(button)
        self.setLayout(layout)
    def change_source(self,i):
        global source
        source = i
        print(source)
    def run(self):
        if source == 1:
            wallbase.getWOTD()
        elif source == 2:
            paperwall.getWOTD()

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())