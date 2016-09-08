# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 11:47:07 2016

@author: Matt
"""

from PyQt4 import Qt
#from nanpy import (SerialManager, ArduinoApi)
from time import sleep
from collections import OrderedDict
import time
import numpy as np

class CameraWizard(Qt.QWizard):
    NUM_PAGES = 4

    (PageCameraConnect, PageTrackingMethods, PageBSCalibration, PageCTCalibration) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(CameraWizard, self).__init__(parent)

        self.setPage(self.PageCameraConnect, CameraConnectPage(self))
        self.setPage(self.PageTrackingMethods, TrackingMethodsPage())
        self.setPage(self.PageBSCalibration, BSCalibrationPage())
        self.setPage(self.PageCTCalibration, CTCalibrationPage())

        self.setStartId(self.PageCameraConnect)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        #self.setPixmap(Qt.QWizard.LogoPixmap, Qt.QPixmap("giphy.gif"))

        self.setWindowTitle(self.tr("Camera Wizard"))

class CameraConnectPage(Qt.QWizardPage):
    def __init__(self, parent=None):
        super(CameraConnectPage, self).__init__(parent)

        self.setTitle(self.tr("Establish Connection to Raspberry Pi Camera Module"))
        #self.setPixmap(Qt.QWizard.WatermarkPixmap, Qt.QPixmap("rpilogo.png"))
        topLabel = Qt.QLabel(self.tr("Attempt to establish a connection to your Raspberry Pi Camera Module"))
        topLabel.setWordWrap(True)

        self.regRBtn = Qt.QRadioButton(self.tr("&Attempt to establish a connection to your Raspberry Pi Camera Module"))
        self.regRBtn.setChecked(False)
        self.regRBtn.clicked.connect(self.connect_to_camera)

        self.registerField("Camera Connected?*", self.regRBtn)

        self.camera_resolution = (480,320)
        self.camera_framerate = 15

        layout = Qt.QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(self.regRBtn)
        self.setLayout(layout)

    def nextId(self):
        return CameraWizard.PageTrackingMethods

    def connect_to_camera(self):
        try:
            from picamera.array import PiRGBArray
            from picamera import PiCamera
            import cv2
            global camera
            camera = PiCamera()
        except:
            print("Failed to connect to Camera")
            self.regRBtn.setChecked(True)               # change back to False

class TrackingMethodsPage(Qt.QWizardPage):
    def selection_change(self):
        if self.cmBox.currentText() == "Background Subtraction":
            self.txEdt.setText("Background Subtraction Method. Suited for when the mouse is not going to be stationary for long periods of time")
        elif self.cmBox.currentText() == "Colour Tracking":
            self.txEdt.setText("Colour Tracking Method. Suited for when the lighting conditions aren't likely to change. Requires calibration. Can track multiple animals")
        else:
            self.txEdt.clear()    
    
    def __init__(self, parent=None):
        super(TrackingMethodsPage, self).__init__(parent)

        self.setTitle(self.tr("Locomotion Tracking Methods"))
        #self.setSubTitle(self.tr(""))

        self.cmBox = Qt.QComboBox()
        self.cmBox.addItems(["", "Background Subtraction", "Colour Tracking"])
        
        self.cmBox.currentIndexChanged.connect(self.selection_change)
        
        self.txEdt = Qt.QTextEdit()
        self.txEdt.setReadOnly(True)
        
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.cmBox)
        layout.addWidget(self.txEdt)
        
        self.setLayout(layout)

    def nextId(self):
        if self.cmBox.currentText() == "Background Subtraction":
            return CameraWizard.PageBSCalibration
        elif self.cmBox.currentText() == "Colour Tracking":
            return CameraWizard.PageCTCalibration
            
class BSCalibrationPage(Qt.QWizardPage):
    def pixels_to_millimetres(self):
        global ref
        from live_colour_calib import pixels_to_mm
        ref = pixels_to_mm()
        print(ref)        
            
    def calib_background_subtraction(self):
        global calib
        from live_colour_calib import live_contour_calib
        calib = live_contour_calib()
        print(calib)
        
    def __init__(self, parent=None):
        super(BSCalibrationPage, self).__init__(parent)

        self.setTitle(self.tr("Calibrate the Camera!"))
        self.setSubTitle(self.tr("Calibrate your camera for the background subtraction method"))
        
        pshBtn1 = Qt.QPushButton(self.tr("Pixels to Millimetres"))
        pshBtn1.clicked.connect(self.pixels_to_millimetres)
        
        pshBtn2 = Qt.QPushButton(self.tr("Calibrate Background Subtraction"))
        pshBtn2.clicked.connect(self.calib_background_subtraction)
        
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(pshBtn1)
        layout.addWidget(pshBtn2)
        
    def nextId(self):
        return -1

class CTCalibrationPage(Qt.QWizardPage):
    def pixels_to_millimetres(self):
        global ref
        from live_colour_calib import pixels_to_mm
        ref = pixels_to_mm()
        print(ref)
    
    def calib_colour_tracking(self):
        global calib
        from live_colour_calib import live_colour_calib
        calib = live_colour_calib()
        print(calib)
                   
    def __init__(self, parent=None):
        super(CTCalibrationPage, self).__init__(parent)
        
        self.setTitle(self.tr("Calibrate your Camera!"))
        self.setSubTitle(self.tr("Calibrate your camera for the colour tracking method"))
        
        pshBtn1 = Qt.QPushButton(self.tr("Pixels to Millimetres"))
        pshBtn1.clicked.connect(self.pixels_to_millimetres)
        
        pshBtn2 = Qt.QPushButton(self.tr("Calibrate Colour Tracking"))
        pshBtn2.clicked.connect(self.calib_colour_tracking)
        
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(pshBtn1)
        layout.addWidget(pshBtn2)
        
    def nextId(self):
        return -1


# main ============================================================================================================================================================================

def main():
    import sys

    app = Qt.QApplication(sys.argv)
    cwiz = CameraWizard()
    cwiz.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()











