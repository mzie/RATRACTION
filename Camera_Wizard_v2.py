# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 11:47:07 2016

@author: Matt
"""

from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
from time import sleep
from collections import OrderedDict
import cv2
import time
import numpy as np
import sys
from vid_tracking_methods import (live_pixels_to_cm, vid_pixels_to_cm,
                                  live_capture_ref_image, vid_capture_ref_image,
                                  live_colour_calib, vid_colour_calib)

class ButtonLineEdit(Qt.QLineEdit):
    buttonClicked = Qt.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = Qt.QToolButton(self)
        self.button.setIcon(Qt.QIcon('open_file_icon.png'))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)

class CameraWizard(Qt.QWizard):
    NUM_PAGES = 4

    (PageTrackingMethods, PageCalibration0, PageCalibration1, PageCalibration2) = range(NUM_PAGES)

    def __init__(self, cam, vid_name, vidTrack_sp, parent=None):
        super(CameraWizard, self).__init__(parent)

        global vidTrack_setup_parameters
        vidTrack_setup_parameters = vidTrack_sp

        self.cam = cam
        self.vid_name = vid_name

        self.setPage(self.PageTrackingMethods, TrackingMethodsPage(self))
        self.setPage(self.PageCalibration0, CalibrationPage0())
        self.setPage(self.PageCalibration1, CalibrationPage1(cam, vid_name))
        self.setPage(self.PageCalibration2, CalibrationPage2(cam, vid_name))

        self.setStartId(self.PageTrackingMethods)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ClassicStyle)
        self.setOption(self.HaveHelpButton, True)

        self.setWindowTitle(self.tr("Video Tracking Setup Wizard"))

class TrackingMethodsPage(Qt.QWizardPage):
      
    def __init__(self, parent=None):
        super(TrackingMethodsPage, self).__init__(parent)

        global vidTrack_setup_parameters

        self.setTitle(self.tr("Locomotion Tracking Methods"))

        self.cmBox1 = Qt.QComboBox()

        tracking_algorithms = ["No tracking algorithm", "Tracking algorithm using frame differencing", "Tracking algorithm using MOG"]

        self.tracking_algorithms_description = {"Tracking algorithm using frame differencing":"Tracking algorithm using frame differencing. Faster and more accurate but requires a reference image of the arena without the animal in it."
                "Will mistakenly track objects which are the same colour as the animal being tracked that have moved since the time the reference image was taken.",
                                            "Tracking algorithm using MOG":"Tracking algorithm using MOG. Slower and less accurate than the frame differencing algorithm but doesn't require a reference image"
                               "of the arena without the animal in it. Therefore this algorithm can be used applied to videos for which an appropriate reference image"
                               "can't be taken. Can account for the movement of objects inside the arena.", "No tracking algorithm":"No tracking algorithm will be applied to the live camera/video feed. This option should be used when "
                                "the animal is to be remotely observed and its behaviour manually recorded. Without the additional processing requried for the tracking algorithms, the live camera feed will have a higher framerate and the "
                                    "video feed will run faster."}
        
        self.cmBox1.addItems(tracking_algorithms)
        self.cmBox1.currentIndexChanged.connect(self.selection_change)
      
        self.txtEdt1 = Qt.QTextEdit()
        self.txtEdt1.setReadOnly(True)

        self.txtEdt1.setText(self.tracking_algorithms_description[tracking_algorithms[0]])
        
        try:
            if vidTrack_setup_parameters["video_tracking_algorithm"] == "None":
                self.cmBox1.setCurrentIndex(0)
            elif vidTrack_setup_parameters["video_tracking_algorithm"] == "Frame Differencing":
                self.cmBox1.setCurrentIndex(1)
            elif vidTrack_setup_parameters["video_tracking_algorithm"] == "MOG":
                self.cmBox1.setCurrentIndex(2)
        except:
            pass

        layout1 = Qt.QVBoxLayout()
        layout1.addWidget(self.cmBox1)
        layout1.addWidget(self.txtEdt1)
        
        self.setLayout(layout1)
        
    def nextId(self):
        global vidTrack_setup_parameters
        if self.cmBox1.currentText() == "No tracking algorithm":
            try:
                vidTrack_setup_parameters["video_tracking_algorithm"] = "None"
            except:
                vidTrack_setup_parameters = {"video_tracking_algorithm":"None"}
            return CameraWizard.PageCalibration0
        elif self.cmBox1.currentText() == "Tracking algorithm using frame differencing":
            try:
                vidTrack_setup_parameters["video_tracking_algorithm"] = "Frame Differencing"
            except:
                vidTrack_setup_parameters = {"video_tracking_algorithm":"Frame Differencing"}
            return CameraWizard.PageCalibration1
        elif self.cmBox1.currentText() == "Tracking algorithm using MOG":
            try:
                vidTrack_setup_parameters["video_tracking_algorithm"] = "MOG"
            except:
                vidTrack_setup_parameters = {"video_tracking_algorithm":"MOG"}
            return CameraWizard.PageCalibration2
        
    def selection_change(self):
        self.txtEdt1.setText(self.tracking_algorithms_description[self.cmBox1.currentText()])


class CalibrationPage0(Qt.QWizardPage):

    def __init__(self, parent=None):
        super(CalibrationPage0, self).__init__(parent)

        global vidTrack_setup_parameters

        self.setTitle(self.tr("Calibrate the video tracking method!"))
        self.setSubTitle(self.tr("No calibration is requried as no tracking algorithm has been applied"))
    
        self.pshBtn4 = Qt.QPushButton(self.tr("Finalise Calibration"))
        self.pshBtn4.clicked.connect(self.finalise_calibration)

        layout1 = Qt.QVBoxLayout(self)
        layout1.addStretch(0)
        layout1.addWidget(self.pshBtn4)
        layout1.addStretch(0)

    def nextId(self):
        return -1

    def finalise_calibration(self):
        global vidTrack_setup_parameters
        print("new video tracking method: %s" %(vidTrack_setup_parameters))

                   
class CalibrationPage1(Qt.QWizardPage):
        
    def __init__(self, cam, vid_name, parent=None):
        super(CalibrationPage1, self).__init__(parent)

        global vidTrack_setup_parameters

        self.cam = cam
        self.vid_name = vid_name

        self.setTitle(self.tr("Calibrate the video tracking method!"))
        self.setSubTitle(self.tr("Calibrate your camera for the frame differencing video tracking method"))

        boldFont = Qt.QFont()
        boldFont.setBold(True)
       
        lbl1 = Qt.QLabel(self.tr("Arena width (cm):"))
        self.lneEdt1 = Qt.QLineEdit()
        lbl1.setBuddy(self.lneEdt1)
        try:
            self.lneEdt1.setText(str(vidTrack_setup_parameters["ref_col"][2]))
        except:
            pass
                            
        lbl2 = Qt.QLabel(self.tr("Arena height (cm):"))
        self.lneEdt2 = Qt.QLineEdit()
        lbl2.setBuddy(self.lneEdt2)
        try:
            self.lneEdt2.setText(str(vidTrack_setup_parameters["ref_col"][3]))
        except:
            pass

        #self.registerField("Arena width entered*", self.lneEdt1)
        #self.registerField("Arena height entered*", self.lneEdt2)

        self.pshBtn1 = Qt.QPushButton(self.tr("Pixels to Centimetres Calibration"))
        self.pshBtn1.clicked.connect(self.pixels_to_millimetres)

        lbl3 = Qt.QLabel(self.tr("Arena top left corner (origin) X/Y coordinates (pixels):"))
        self.lneEdt3 = Qt.QLineEdit()
        self.lneEdt3.setReadOnly(True)
        lbl3.setBuddy(self.lneEdt3)
        try:
            self.lneEdt3.setText(str(vidTrack_setup_parameters["ref_col"][0]))
        except:
            pass

        lbl4 = Qt.QLabel(self.tr("Arena bottom right corner X/Y coordinates (pixels):"))
        self.lneEdt4 = Qt.QLineEdit()
        self.lneEdt4.setReadOnly(True)
        lbl4.setBuddy(self.lneEdt4)
        try:
            self.lneEdt4.setText(str(vidTrack_setup_parameters["ref_col"][1]))
        except:
            pass

        lbl5 = Qt.QLabel(self.tr("Number of centimetres per pixel for the arena width:"))
        self.lneEdt5 = Qt.QLineEdit()
        self.lneEdt5.setReadOnly(True)
        lbl5.setBuddy(self.lneEdt5)
        try:
            self.lneEdt5.setText(str(vidTrack_setup_parameters["ref_col"][4]))
        except:
            pass

        lbl6 = Qt.QLabel(self.tr("Number of centimetres per pixel for the arena width:"))
        self.lneEdt6 = Qt.QLineEdit()
        self.lneEdt6.setReadOnly(True)
        lbl6.setBuddy(self.lneEdt6)
        try:
            self.lneEdt6.setText(str(vidTrack_setup_parameters["ref_col"][5]))
        except:
            pass

        lbl7 = Qt.QLabel(self.tr("Load Reference Image:"))
        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.buttonClicked.connect(self.load_reference_image)
        lbl7.setBuddy(self.btnLneEdt1)
        try:
            self.btnLneEdt1.setText(vidTrack_setup_parameters["reference_image_name"])
        except:
            pass

        lbl8 = Qt.QLabel(self.tr("OR"))
        lbl8.setFont(boldFont)

        lbl9 = Qt.QLabel(self.tr("Capture Reference Image:"))
        self.lneEdt7 = Qt.QLineEdit()
        self.lneEdt7.setText("example_reference_image.png")
        lbl9.setBuddy(self.lneEdt7)
        
        self.pshBtn2 = Qt.QPushButton(self.tr("Capture"))
        self.pshBtn2.clicked.connect(self.capture_reference_image)

        self.pshBtn3 = Qt.QPushButton(self.tr("Colour Calibration"))
        self.pshBtn3.clicked.connect(self.colour_calibration)

        lbl10 = Qt.QLabel(self.tr("Colour threshold lower bound (BGR):"))
        self.lneEdt8 = Qt.QLineEdit()
        self.lneEdt8.setReadOnly(True)
        lbl10.setBuddy(self.lneEdt8)
        try:
            self.lneEdt8.setText(str(vidTrack_setup_parameters["calib_col"][0]))
        except:
            pass

        lbl11 = Qt.QLabel(self.tr("Colour threshold upper bound (BGR):"))
        self.lneEdt9 = Qt.QLineEdit()
        self.lneEdt9.setReadOnly(True)
        lbl11.setBuddy(self.lneEdt8)
        try:
            self.lneEdt9.setText(str(vidTrack_setup_parameters["calib_col"][1]))
        except:
            pass

        self.pshBtn4 = Qt.QPushButton(self.tr("Finalise Calibration"))
        self.pshBtn4.clicked.connect(self.finalise_calibration)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()
        spacer4 = Qt.QLabel()

        layout1 = Qt.QFormLayout()
        layout1.addRow(lbl1, self.lneEdt1)
        layout1.addRow(lbl2, self.lneEdt2)

        layout2 = Qt.QFormLayout()
        layout2.addRow(lbl3, self.lneEdt3)
        layout2.addRow(lbl4, self.lneEdt4)
        layout2.addRow(lbl5, self.lneEdt5)
        layout2.addRow(lbl6, self.lneEdt6)

        layout3 = Qt.QHBoxLayout()
        layout3.addWidget(self.lneEdt7)
        layout3.addWidget(self.pshBtn2)

        layout4 = Qt.QFormLayout()
        layout4.addRow(lbl7, self.btnLneEdt1)
        layout4.addRow(lbl8)
        layout4.addRow(lbl9, layout3)

        layout5 = Qt.QFormLayout()
        layout5.addRow(lbl10, self.lneEdt8)
        layout5.addRow(lbl11, self.lneEdt9)

        layout6 = Qt.QVBoxLayout(self)
        layout6.addLayout(layout1)
        layout6.addWidget(spacer1)
        layout6.addWidget(self.pshBtn1)
        layout6.addLayout(layout2)
        layout6.addWidget(spacer2)
        layout6.addLayout(layout4)
        layout6.addWidget(spacer3)
        layout6.addWidget(self.pshBtn3)
        layout6.addLayout(layout5)
        layout6.addWidget(spacer4)
        layout6.addWidget(self.pshBtn4)
        
    def nextId(self):
        return -1

    def pixels_to_millimetres(self):
        global vidTrack_setup_parameters
        if self.cam != None:
            temp = live_pixels_to_cm(self.cam)
        elif self.vid_name != None:
            temp = vid_pixels_to_cm(self.vid_name)
        pix_width = int(temp[1][0]-temp[0][0])
        pix_height = int(temp[1][1]-temp[0][1])
        cm_width = float(self.lneEdt1.text())
        cm_height = float(self.lneEdt2.text())
        arena_size = (cm_width, cm_height)
        cm_per_pixel_width = round((cm_width/pix_width),3)
        cm_per_pixel_height = round((cm_height/pix_height),3)
        ref_col = (temp[0], temp[1], cm_width, cm_height, cm_per_pixel_width, cm_per_pixel_height)
        vidTrack_setup_parameters["ref_col"] = ref_col
        self.lneEdt3.setText(str(ref_col[0]))
        self.lneEdt4.setText(str(ref_col[1]))
        self.lneEdt5.setText(str(ref_col[4]))
        self.lneEdt6.setText(str(ref_col[5]))

    def load_reference_image(self):
        global vidTrack_setup_parameters
        try:
            self.ref_image_name = Qt.QFileDialog.getOpenFileName(self, 'Load Reference Image')
            self.btnLneEdt1.setText(self.ref_image_name)
            vidTrack_setup_parameters["reference_image_name"] = self.ref_image_name
        except:
            pass

    def capture_reference_image(self):
        global vidTrack_setup_parameters
        self.ref_image_name = self.lneEdt3.text()
        if self.cam != None:
            temp_image = live_capture_ref_image(self.cam, self.ref_image_name)
        elif self.vid_name != None:
            temp_image = vid_capture_ref_image(self.vid_name)
        vidTrack_setup_parameters["reference_image_name"] = self.ref_image_name
    
    def colour_calibration(self):
        global vidTrack_setup_parameters
        if self.cam != None:
            temp = live_colour_calib(self.cam)
        elif self.vid_name != None:
            temp = vid_colour_calib(self.vid_name)
        calib_col = temp
        vidTrack_setup_parameters["calib_col"] = calib_col
        self.lneEdt8.setText(str(calib_col[0]))
        self.lneEdt9.setText(str(calib_col[1]))
        
    def finalise_calibration(self):
        global vidTrack_setup_parameters
        print("new video tracking method: %s" %(vidTrack_setup_parameters))
        
class CalibrationPage2(Qt.QWizardPage):
                   
    def __init__(self, cam, vid_name, parent=None):
        super(CalibrationPage2, self).__init__(parent)

        global vidTrack_setup_parameters

        self.cam = cam
        self.vid_name = vid_name
        
        self.setTitle(self.tr("Calibrate the video tracking method!"))
        self.setSubTitle(self.tr("Calibrate your camera for the MOG video tracking method"))
        
        lbl1 = Qt.QLabel(self.tr("Arena width (cm):"))
        self.lneEdt1 = Qt.QLineEdit()
        lbl1.setBuddy(self.lneEdt1)
        try:
            self.lneEdt1.setText(str(vidTrack_setup_parameters["ref_col"][2]))
        except:
            pass

        lbl2 = Qt.QLabel(self.tr("Arena height (cm):"))
        self.lneEdt2 = Qt.QLineEdit()
        lbl2.setBuddy(self.lneEdt2)
        try:
            self.lneEdt2.setText(str(vidTrack_setup_parameters["ref_col"][3]))
        except:
            pass
    
        #self.registerField("Arena width entered*", self.lneEdt1)
        #self.registerField("Arena height entered*", self.lneEdt2)

        pshBtn1 = Qt.QPushButton(self.tr("Pixels to Centimetres Calibration"))
        pshBtn1.clicked.connect(self.pixels_to_millimetres)

        lbl3 = Qt.QLabel(self.tr("Arena top left corner (origin) X/Y coordinates (pixels):"))
        self.lneEdt3 = Qt.QLineEdit()
        self.lneEdt3.setReadOnly(True)
        lbl3.setBuddy(self.lneEdt3)
        try:
            self.lneEdt3.setText(str(vidTrack_setup_parameters["ref_col"][0]))
        except:
            pass

        lbl4 = Qt.QLabel(self.tr("Arena bottom right corner X/Y coordinates (pixels):"))
        self.lneEdt4 = Qt.QLineEdit()
        self.lneEdt4.setReadOnly(True)
        lbl4.setBuddy(self.lneEdt4)
        try:
            self.lneEdt4.setText(str(vidTrack_setup_parameters["ref_col"][1]))
        except:
            pass

        lbl5 = Qt.QLabel(self.tr("Number of centimetres per pixel for the arena width:"))
        self.lneEdt5 = Qt.QLineEdit()
        self.lneEdt5.setReadOnly(True)
        lbl5.setBuddy(self.lneEdt5)
        try:
            self.lneEdt5.setText(str(vidTrack_setup_parameters["ref_col"][4]))
        except:
            pass

        lbl6 = Qt.QLabel(self.tr("Number of centimetres per pixel for the arena width:"))
        self.lneEdt6 = Qt.QLineEdit()
        self.lneEdt6.setReadOnly(True)
        lbl6.setBuddy(self.lneEdt6)
        try:
            self.lneEdt6.setText(str(vidTrack_setup_parameters["ref_col"][5]))
        except:
            pass
        
        pshBtn2 = Qt.QPushButton(self.tr("Colour Calibration"))
        pshBtn2.clicked.connect(self.colour_calibration)

        lbl7 = Qt.QLabel(self.tr("Colour threshold lower bound (BGR):"))
        self.lneEdt7 = Qt.QLineEdit()
        self.lneEdt7.setReadOnly(True)
        lbl7.setBuddy(self.lneEdt7)
        try:
            self.lneEdt7.setText(str(vidTrack_setup_parameters["calib_col"][0]))
        except:
            pass

        lbl8 = Qt.QLabel(self.tr("Colour threshold upper bound (BGR):"))
        self.lneEdt8 = Qt.QLineEdit()
        self.lneEdt8.setReadOnly(True)
        lbl8.setBuddy(self.lneEdt8)
        try:
            self.lneEdt8.setText(str(vidTrack_setup_parameters["calib_col"][1]))
        except:
            pass

        self.pshBtn3 = Qt.QPushButton(self.tr("Finalise Calibration"))
        self.pshBtn3.clicked.connect(self.finalise_calibration)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()

        layout1 = Qt.QFormLayout()
        layout1.addRow(lbl1, self.lneEdt1)
        layout1.addRow(lbl2, self.lneEdt2)

        layout2 = Qt.QFormLayout()
        layout2.addRow(lbl3, self.lneEdt3)
        layout2.addRow(lbl4, self.lneEdt4)
        layout2.addRow(lbl5, self.lneEdt5)
        layout2.addRow(lbl6, self.lneEdt6)

        layout3 = Qt.QFormLayout()
        layout3.addRow(lbl7, self.lneEdt7)
        layout3.addRow(lbl8, self.lneEdt8)
        
        layout4 = Qt.QVBoxLayout(self)
        layout4.addLayout(layout1)
        layout4.addWidget(spacer1)
        layout4.addWidget(pshBtn1)
        layout4.addLayout(layout2)
        layout4.addWidget(spacer2)
        layout4.addWidget(pshBtn2)
        layout4.addLayout(layout3)
        layout4.addWidget(spacer3)
        layout4.addWidget(self.pshBtn3)

    def nextId(self):
        return -1

    def pixels_to_millimetres(self):
        global vidTrack_setup_parameters
        if self.cam != None:
            temp = live_pixels_to_cm(self.cam)
        elif self.vid_name != None:
            temp = vid_pixels_to_cm(self.vid_name)
        pix_width = int(temp[1][0]-temp[0][0])
        pix_height = int(temp[1][1]-temp[0][1])
        cm_width = float(self.lneEdt1.text())
        cm_height = float(self.lneEdt2.text())
        arena_size = (cm_width, cm_height)
        cm_per_pixel_width = round((cm_width/pix_width),3)
        cm_per_pixel_height = round((cm_height/pix_height),3)
        ref_col = (temp[0], temp[1], cm_width, cm_height, cm_per_pixel_width, cm_per_pixel_height)
        vidTrack_setup_parameters["ref_col"] = ref_col
        self.lneEdt3.setText(str(ref_col[0]))
        self.lneEdt4.setText(str(ref_col[1]))
        self.lneEdt5.setText(str(ref_col[4]))
        self.lneEdt6.setText(str(ref_col[5]))
    
    def colour_calibration(self):
        global vidTrack_setup_parameters
        if self.cam != None:
            temp = live_colour_calib(self.cam)
        elif self.vid_name != None:
            temp = vid_colour_calib(self.vid_name)
        calib_col = temp
        vidTrack_setup_parameters["calib_col"] = calib_col
        self.lneEdt7.setText(str(calib_col[0]))
        self.lneEdt8.setText(str(calib_col[1]))

    def finalise_calibration(self):
        global vidTrack_setup_parameters
        print("new video tracking method: %s" %(vidTrack_setup_parameters))

      
# main ===========================================

def main():
    app = Qt.QApplication(sys.argv)
    cwiz = CameraWizard()
    cwiz.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
