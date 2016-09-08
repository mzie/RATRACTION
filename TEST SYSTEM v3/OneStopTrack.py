# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 00:09:18 2016

@author: Matt
"""

from PyQt4 import Qt
import Arduino_Wizard
import Camera_Wizard_v2
from time import sleep

class Window(Qt.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.button1 = Qt.QPushButton(self)
        self.button1.setFixedSize(200,200)
        self.button1.setIcon(Qt.QIcon('rpilogo.png'))
        self.button1.setIconSize(Qt.QSize(175,175))
        self.button1.clicked.connect(self.handleButton2) 
        
        self.button2 = Qt.QPushButton(self)
        self.button2.setFixedSize(200,200)
        self.button2.setIcon(Qt.QIcon('ardlogo.png'))
        self.button2.setIconSize(Qt.QSize(150,150))
        self.button2.clicked.connect(self.handleButton1)
        
        self.button3 = Qt.QPushButton(self)
        self.button3.setFixedSize(100,100)
        self.button3.setIcon(Qt.QIcon('Green_Start.png'))
        self.button3.setIconSize(Qt.QSize(75,75))
        self.button3.clicked.connect(self.ard_start)  
        
        self.button4 = Qt.QPushButton(self)
        self.button4.setFixedSize(100,100)
        self.button4.setIcon(Qt.QIcon('Red_Stop.png'))
        self.button4.setIconSize(Qt.QSize(75,75))
        self.button4.clicked.connect(self.ard_stop)  
        
        self.button5 = Qt.QPushButton(self)
        self.button5.setFixedSize(100,100)
        self.button5.setIcon(Qt.QIcon('Circle_Start.png'))
        self.button5.setIconSize(Qt.QSize(75,75))
        self.button5.clicked.connect(self.cam_start) 

        self.table = Qt.QTableWidget(self)
        self.table.setRowCount(1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Test #', 'Date', 'Start Time', 'End Time', 'Comments'])
        #self.table.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
            
        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.button3)
        layout1.addWidget(self.button4)
        layout1.addWidget(self.button5)
        layout1.addStretch(True)

        layout2 = Qt.QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.table)

        layout3 = Qt.QVBoxLayout()
        layout3.addWidget(self.button1)
        layout3.addWidget(self.button2)
        layout3.addStretch(True)

        layout4 = Qt.QHBoxLayout()
        layout4.addLayout(layout3)
        layout4.addLayout(layout2)
        
        self.setLayout(layout4)
      
        self.ardstarted = False
        self.camstarted = False
        
        global results
        results = {'TIME':[0,1,2,3,4,5,6,7,8,9], 'DISTANCE':[0,5,10,15,20,25,30,35], 'VELOCITY':[0,2,4,6,8,10,12,14]}          
       
    def handleButton1(self):
        self.awiz = Arduino_Wizard.ArduinoWizard()
        self.awiz.show()
        
    def handleButton2(self):
        self.cwiz = Camera_Wizard_v2.CameraWizard()
        self.cwiz.show()

    def ard_start(self):
        if not self.ardstarted:
            self.ardstarted = True
            self.StartArdLoop()
        
    def ard_stop(self):  
        if self.ardstarted:
            self.ardstarted = False

    def StartArdLoop(self):
        #global a, assu, setu, loopu
        #from Arduino_Wizard import (a, assu, setu, loopu)
        global ard_results
        ard_results = {'2':[0,1,2,3,4,5,6,7,8,9,10]}
        #exec(assu)
        #exec(setu)
        while self.ardstarted:
#        print(assu)
#        print(setu)
#        print(loopu)
            #exec(loopu)
            sleep(1)
            print("hello")
            Qt.qApp.processEvents()       

    def cam_start(self):
#        if self.camstarted:
#            self.camstarted = True
        global calib
        from Camera_Wizard_v2 import calib
        from live_colour_calib import live_colour_tracking
        self.pts = live_colour_tracking(calib[0],calib[1])


def main():
    import sys
    
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())    

if __name__ == '__main__':
    main()
