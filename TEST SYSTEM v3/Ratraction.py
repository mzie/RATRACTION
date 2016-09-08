# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:54:18 2016

@author: Matt
"""

from PyQt4 import Qt
#from PyQt4.QtCore import Qt as QT
#from PyQt4.QtGui import QWidget, QApplication, QSplitter, QLabel, QVBoxLayout
from time import sleep
import OneStopTrack
import qtab_demo
import plot_demo

class MyWindow(Qt.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.initUI()
        
        main_widget = OneStopTrack.Window()
                      
        self.setCentralWidget(main_widget)
        self.show()
        
        Qt.QApplication.setStyle(Qt.QStyleFactory.create('Cleanlooks'))
#        Qt.QApplication.setStyle(Qt.QStyleFactory.create('Windows')) 

      
    def initUI(self):               
        
        exitAction = Qt.QAction("&Quit", self)
        #exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openResults = Qt.QAction("&Raw Data", self)
        openResults.triggered.connect(self.get_results)  

        plotResults = Qt.QAction("&Plot", self)
        plotResults.triggered.connect(self.plot_results)  

        processResults = Qt.QAction("&IR break beam", self)
        processResults.triggered.connect(self.process_results)

        #self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        resultsMenu = menubar.addMenu("&Results")
        resultsMenu.addAction(openResults)
        
        plotMenu = menubar.addMenu("&Plots")        
        plotMenu.addAction(plotResults)        
        
        processingMenu = menubar.addMenu("&Data Processing")
        processingMenu.addAction(processResults)
                
        self.setGeometry(50, 50, 900, 300)
        self.setMinimumWidth(900)
        self.setWindowTitle(self.tr("RATRACTION"))
        self.show()
        
        
    def get_results(self):
        self.results = qtab_demo.Table()
        self.results.show()
        
    def plot_results(self):
        self.plot = plot_demo.Plot()
        self.plot.show()

    def process_results(self):
        pass

def main():
    import sys
    app = Qt.QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()	