# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 00:09:18 2016

@author: Matt
"""
# import necessary packages and modules
from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from time import strftime
import time
import datetime
import time
import sys
import cv2
from collections import (deque, OrderedDict)
from picamera.array import PiRGBArray
from picamera import PiCamera
import vid_tracking_methods
import Arduino_Wizard_v2
import Camera_Wizard_v2
import setup_arena_picture

class EmittingStream(Qt.QObject):
    textWritten = Qt.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

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

class VideoTracking(Qt.QObject):
    """
    Object managing running the video tracking code
    """
 
    def __init__(self):
        super(VideoTracking, self).__init__()
        global _isRunning
        _isRunning = True
         
    def Run(self):
        global _isRunning, vidTrack_setup_parameters, camera, video_name, recording, record_name

        if not _isRunning:
            _isRunning = True

        date = strftime("%Y-%m-%d")
        start_time = strftime("%H:%M:%S")

        try:
            if vidTrack_setup_parameters == None:
                try:
                    from Camera_Wizard_v2 import vidTrack_setup_parameters
                except:
                    pass
            if camera:
                if vidTrack_setup_parameters['video_tracking_algorithm'] == "MOG":
                    if not recording:
                        live_trck = vid_tracking_methods.live_mog_tracking(camera, vidTrack_setup_parameters)
                        return live_trck
                    elif recording and vidTrack_setup_parameters != None:
                        live_trck = vid_tracking_methods.live_mog_tracking(camera, vidTrack_setup_parameters, recording, record_name)
                        return live_trck
                elif vidTrack_setup_parameters['video_tracking_algorithm'] == "Frame Differencing":
                    if not recording:
                        live_trck = vid_tracking_methods.live_fd_tracking(camera, vidTrack_setup_parameters)
                        return live_trck
                    elif recording and vidTrack_setup_parameters != None:
                        live_trck = vid_tracking_methods.live_fd_tracking(camera, vidTrack_setup_parameters, recording, record_name)
                        return live_trck
                elif vidTrack_setup_parameters['video_tracking_algorithm'] == "None":
                    if not recording:
                        live_cam_feed = vid_tracking_methods.live_camera_feed(camera)
                        return live_cam_feed
                    elif recording:
                        live_cam_feed = vid_tracking_methods.live_camera_feed(camera, recording, record_name)
                        return record_video
                        
            elif video_name:
                if vidTrack_setup_parameters['video_tracking_algorithm'] == "MOG":
                    vid_trck = vid_tracking_methods.vid_mog_tracking(video_name, vidTrack_setup_parameters)
                    return vid_trck
                elif vidTrack_setup_parameters['video_tracking_algorithm'] == "Frame Differencing":
                    vid_trck = vid_tracking_methods.vid_fd_tracking(video_name, vidTrack_setup_parameters)
                    return vid_trck
                elif vidTrack_setup_parameters['video_tracking_algorithm'] == "None": 
                    vid_feed = vid_tracking_methods.video_feed(video_name)
                    return vid_feed
            else:
                print("video tracking method is either missing or contains an error/s")
        except:
            print("video tracking method is either missing or contains an error/s")
                                   
    def stop(self):
        global _isRunning
        _isRunning = False 

class Arduino(Qt.QObject):
    """
    Object managing running the Arduino code
    """
 
    def __init__(self):
        super(Arduino, self).__init__()
        global _isRunning2
        _isRunning2 = True

        self.actButton1_on = False
        self.actButton2_on = False
        self.actButton3_on = False
        self.actButton4_on = False
        self.actButton5_on = False
        self.actButton6_on = False
        self.actButton7_on = False
        self.actButton8_on = False
 
    def Run(self):
        global ard_results, _isRunning2, ard_setup_parameters, a, mod_pt
        
        ard_results = {}
        
        if not _isRunning2:
            _isRunning2 = True      

        try:
            if ard_setup_parameters == None:
                try:
                    from Arduino_Wizard_v2 import ard_setup_parameters
                except:
                    pass
            pins = ard_setup_parameters['pins']
            naming_list = ard_setup_parameters['naming_list']
            setup_list = ard_setup_parameters['setup_list']
            loop_list = ard_setup_parameters['loop_list']
            
            for key in pins.keys():
                ard_results[pins[key][0]] = []
            ard_results['ard_loop_time'] = []

            for name in naming_list:
                exec(name)
            
            for line in setup_list:
                exec(line)
    
            start = float(time.time())

            while _isRunning2:
                millis = float(time.time())
                current_loop_time = millis - start
                ard_results['ard_loop_time'].append(round(current_loop_time, 2))
                for line in loop_list:

                    try:
                        exec(line)
                    except:
                        continue

            for key in pins.keys():
                if pins[key][1] == "OUTPUT":
                    exec("a.digitalWrite(%s, a.LOW)" %(pins[key][0]))
        except:
            print("arduino method is either missing or contains an error/s")
                          
    def stop(self):
        global _isRunning2
        _isRunning2 = False

    def actButton1(self, checked):
        if checked:
            self.actButton1_on = True
        elif not checked:
            self.actButton1_on = False

    def actButton2(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False 

    def actButton3(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False

    def actButton4(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False

    def actButton5(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False 
    
    def actButton6(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False

    def actButton7(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False

    def actButton8(self, checked):
        if checked:
            self.actButton2_on = True
        elif not checked:
            self.actButton2_on = False 

class Window(Qt.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.startButton = Qt.QPushButton()
        self.startButton.setFixedSize(100,100)
        self.startButton.setIcon(Qt.QIcon('Green_Start.png'))
        self.startButton.setIconSize(Qt.QSize(75,75))

        self.stopButton = Qt.QPushButton()
        self.stopButton.setFixedSize(100,100)
        self.stopButton.setIcon(Qt.QIcon('Red_Stop.png'))
        self.stopButton.setIconSize(Qt.QSize(75,75))

        self.vidThread = Qt.QThread()
        self.ardThread = Qt.QThread()
        self.vidThread.start()
        self.ardThread.start()

        self.vidTracking = VideoTracking()
        self.vidTracking.moveToThread(self.vidThread)

        self.arduino = Arduino()
        self.arduino.moveToThread(self.ardThread)

        self.stopButton.clicked.connect(lambda: self.arduino.stop())
        self.stopButton.clicked.connect(lambda: self.vidTracking.stop())
        self.startButton.clicked.connect(self.arduino.Run)
        self.startButton.clicked.connect(self.start_pressed)                             
        
        self.table = Qt.QTableWidget()
        self.table_rowCount = 0
        self.table.setRowCount(self.table_rowCount)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Trial #', 'Date', 'Start Time', 'End Time', 'Duration (sec)', 'Comments'])
        #self.table.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.cellChanged.connect(self.cell_was_clicked)

        boldFont = Qt.QFont()
        boldFont.setBold(True)

        label1 = Qt.QLabel("Python Console Output")
        label1.setFont(boldFont)

        self.txtEdt1 = Qt.QTextEdit()
        self.txtEdt1.setReadOnly(True)

        # Install the custom output stream
        sys.stdout = EmittingStream(textWritten = self.normalOutputWritten)

        self.actButton1 = Qt.QPushButton(self.tr("&actButton1"))
        self.actButton1.setCheckable(True)
        self.actButton1.toggled.connect(lambda: self.arduino.actButton1(self.actButton1.isChecked()))
        self.actButton2 = Qt.QPushButton(self.tr("&actButton2"))
        self.actButton2.setCheckable(True)
        self.actButton2.toggled.connect(lambda: self.arduino.actButton2(self.actButton2.isChecked()))
        self.actButton3 = Qt.QPushButton(self.tr("&actButton3"))
        self.actButton3.setCheckable(True)
        self.actButton3.toggled.connect(lambda: self.arduino.actButton3(self.actButton3.isChecked()))
        self.actButton4 = Qt.QPushButton(self.tr("&actButton4"))
        self.actButton4.setCheckable(True)
        self.actButton4.toggled.connect(lambda: self.arduino.actButton4(self.actButton4.isChecked()))
        self.actButton5 = Qt.QPushButton(self.tr("&actButton5"))
        self.actButton5.setCheckable(True)
        self.actButton5.toggled.connect(lambda: self.arduino.actButton5(self.actButton5.isChecked()))
        self.actButton6 = Qt.QPushButton(self.tr("&actButton6"))
        self.actButton6.setCheckable(True)
        self.actButton6.toggled.connect(lambda: self.arduino.actButton6(self.actButton6.isChecked()))
        self.actButton7 = Qt.QPushButton(self.tr("&actButton7"))
        self.actButton7.setCheckable(True)
        self.actButton7.toggled.connect(lambda: self.arduino.actButton7(self.actButton7.isChecked()))
        self.actButton8 = Qt.QPushButton(self.tr("&actButton8"))
        self.actButton8.setCheckable(True)
        self.actButton8.toggled.connect(lambda: self.arduino.actButton8(self.actButton8.isChecked()))

        self.frame4 = Qt.QFrame()
        self.frame4.setFrameStyle(1)
        self.frame4.setFixedSize(350,375)

        self.arena_setup_new_edit = Qt.QPushButton("New/Edit")
        self.arena_setup_new_edit.clicked.connect(self.new_edit_arena_setup)

        self.arena_setup_load = Qt.QPushButton("Load")
        self.arena_setup_load.clicked.connect(self.load_arena_setup)

        self.arena_setup_save = Qt.QPushButton("Save")
        self.arena_setup_save.clicked.connect(self.save_arena_setup)
        
        layout6 = Qt.QHBoxLayout()
        layout6.addWidget(self.arena_setup_new_edit)
        layout6.addWidget(self.arena_setup_load)
        layout6.addWidget(self.arena_setup_save)

        self.main_frame = Qt.QWidget()
        self.main_frame.setFixedSize(325,325)
        self.fig = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.fig.canvas.mpl_connect("motion_notify_event", self.mouse_movement)

        self.fig_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        self.fig_toolbar.hide()

        self.homeBtn = Qt.QPushButton()
        self.homeBtn.setFixedSize(25,25)
        self.homeBtn.setIcon(Qt.QIcon('home.png'))
        self.homeBtn.setIconSize(Qt.QSize(20,20))
        self.homeBtn.clicked.connect(self.home)

        self.panBtn = Qt.QPushButton()
        self.panBtn.setCheckable(True)
        self.panBtn.setFixedSize(25,25)
        self.panBtn.setIcon(Qt.QIcon('move.png'))
        self.panBtn.setIconSize(Qt.QSize(20,20))
        self.panBtn.clicked.connect(self.pan)       

        self.zoomBtn = Qt.QPushButton()
        self.zoomBtn.setCheckable(True)
        self.zoomBtn.setFixedSize(25,25)
        self.zoomBtn.setIcon(Qt.QIcon('zoom_to_rect.png'))
        self.zoomBtn.setIconSize(Qt.QSize(20,20))
        self.zoomBtn.clicked.connect(self.zoom_to_rect)

        self.lblsBtn = Qt.QPushButton()
        self.lblsBtn.setCheckable(True)
        self.lblsBtn.setFixedSize(25,25)
        self.lblsBtn.setIcon(Qt.QIcon('label_icon.png'))
        self.lblsBtn.setIconSize(Qt.QSize(20,20))
        self.lblsBtn.clicked.connect(self.show_hide_labels)

        self.drawBtn = Qt.QPushButton()
        self.drawBtn.setFixedSize(25,25)
        self.drawBtn.setIcon(Qt.QIcon('refresh_icon.jpeg'))
        self.drawBtn.setIconSize(Qt.QSize(20,20))
        self.drawBtn.clicked.connect(self.redraw_arena_setup)

        self.coords_label = Qt.QLabel()
        self.coords_label.setAlignment(QtCore.Qt.AlignCenter)

        self.fig_statusbar = Qt.QStatusBar()
        self.fig_statusbar.setSizeGripEnabled(False)
        self.fig_statusbar.addWidget(self.homeBtn)
        self.fig_statusbar.addWidget(self.panBtn)
        self.fig_statusbar.addWidget(self.zoomBtn)
        self.fig_statusbar.addWidget(self.lblsBtn)
        self.fig_statusbar.addWidget(self.drawBtn)
        self.fig_statusbar.addWidget(self.coords_label, 1)

        frame_layout4 = Qt.QVBoxLayout()
        frame_layout4.addLayout(layout6)
        frame_layout4.addWidget(self.main_frame)
        frame_layout4.addWidget(self.fig_statusbar)
        self.frame4.setLayout(frame_layout4)

        self.radBtn1 = Qt.QRadioButton(self.tr("Connect to Raspberry Pi Camera"))
        self.radBtn1.setFont(boldFont)
        self.radBtn1.setChecked(False)  
        self.radBtn1.toggled.connect(self.connect_to_camera)

        self.radBtn4 = Qt.QRadioButton(self.tr("Video Record Trial"))
        self.radBtn4.setChecked(False)
        self.radBtn4.setDisabled(True)
        self.radBtn4.toggled.connect(self.video_record_trial)

        self.lneEdt1 = Qt.QLineEdit()
        self.lneEdt1.setDisabled(True)
        self.lneEdt1.setText("example_video_name.mp4")

        self.lneEdt1.textChanged.connect(self.video_record_trial)

        self.new_edit1 = Qt.QPushButton("New/Edit")
        self.new_edit1.clicked.connect(self.new_edit_video_tracking_method)
        self.new_edit1.setDisabled(True)

        self.load1 = Qt.QPushButton("Load")
        self.load1.clicked.connect(self.load_video_tracking_method)
        self.load1.setDisabled(True)

        self.save1 = Qt.QPushButton("Save")
        self.save1.clicked.connect(self.save_video_tracking_method)
        self.save1.setDisabled(True)
    
        butLayout1 = Qt.QHBoxLayout()
        butLayout1.addWidget(self.new_edit1)
        butLayout1.addWidget(self.load1)
        butLayout1.addWidget(self.save1)

        self.frame1 = Qt.QFrame()
        self.frame1.setFrameStyle(1)
        self.frame1.setFixedSize(350,150)

        frame_layout1 = Qt.QVBoxLayout()
        frame_layout1.addWidget(self.radBtn1)
        frame_layout1.addLayout(butLayout1)
        frame_layout1.addWidget(self.radBtn4)
        frame_layout1.addWidget(self.lneEdt1)
        self.frame1.setLayout(frame_layout1)

        self.radBtn2 = Qt.QRadioButton(self.tr("Load Video Recording"))
        self.radBtn2.setFont(boldFont)
        self.radBtn2.setChecked(False)  
        self.radBtn2.toggled.connect(self.load_video_recording)

        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.setReadOnly(True)
        self.btnLneEdt1.setDisabled(True)
        self.btnLneEdt1.buttonClicked.connect(self.find_video_recording)

        self.new_edit2 = Qt.QPushButton("New/Edit")
        self.new_edit2.clicked.connect(self.new_edit_video_tracking_method)
        self.new_edit2.setDisabled(True)

        self.load2 = Qt.QPushButton("Load")
        self.load2.clicked.connect(self.load_video_tracking_method)
        self.load2.setDisabled(True)

        self.save2 = Qt.QPushButton("Save")
        self.save2.clicked.connect(self.save_video_tracking_method)
        self.save2.setDisabled(True)
    
        butLayout2 = Qt.QHBoxLayout()
        butLayout2.addWidget(self.new_edit2)
        butLayout2.addWidget(self.load2)
        butLayout2.addWidget(self.save2)

        self.frame2 = Qt.QFrame()
        self.frame2.setFrameStyle(1)
        self.frame2.setFixedSize(350,150)

        frame_layout2 = Qt.QVBoxLayout()
        frame_layout2.addWidget(self.radBtn2)
        frame_layout2.addWidget(self.btnLneEdt1)
        frame_layout2.addLayout(butLayout2)
        self.frame2.setLayout(frame_layout2)

        self.radBtn3 = Qt.QRadioButton(self.tr("Connect to Arduino"))
        self.radBtn3.setFont(boldFont)
        self.radBtn3.setChecked(False)  
        self.radBtn3.toggled.connect(self.connect_to_arduino)

        self.new_edit3 = Qt.QPushButton("New/Edit")
        self.new_edit3.clicked.connect(self.new_edit_ard_method)
        self.new_edit3.setDisabled(True)

        self.load3 = Qt.QPushButton("Load")
        self.load3.clicked.connect(self.load_ard_method)
        self.load3.setDisabled(True)

        self.save3 = Qt.QPushButton("Save")
        self.save3.clicked.connect(self.save_ard_method)
        self.save3.setDisabled(True)
    
        butLayout3 = Qt.QHBoxLayout()
        butLayout3.addWidget(self.new_edit3)
        butLayout3.addWidget(self.load3)
        butLayout3.addWidget(self.save3)

        self.frame3 = Qt.QFrame()
        self.frame3.setFrameStyle(1)
        self.frame3.setFixedSize(350,100)

        frame_layout3 = Qt.QVBoxLayout()
        frame_layout3.addWidget(self.radBtn3)
        frame_layout3.addLayout(butLayout3)
        self.frame3.setLayout(frame_layout3)

        self.group = Qt.QButtonGroup()
        self.group.addButton(self.radBtn1)
        self.group.addButton(self.radBtn2)
        self.group.setExclusive(False)
                                       
        self.lcd = QtGui.QLCDNumber()
        self.lcd.setFixedSize(140,40)

        self.frame6 = Qt.QFrame()
        self.frame6.setFrameStyle(1)

        frame_layout6 = Qt.QHBoxLayout()
        frame_layout6.addWidget(self.lcd)
        self.frame6.setLayout(frame_layout6)
 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_time)

        global s, m, h
        s = 0
        m = 0
        h = 0

        layout = Qt.QGridLayout()
        layout.addWidget(self.actButton1, 0, 0)
        layout.addWidget(self.actButton2, 1, 0)
        layout.addWidget(self.actButton3, 0, 1)
        layout.addWidget(self.actButton4, 1, 1)
        layout.addWidget(self.actButton5, 0, 2)
        layout.addWidget(self.actButton6, 1, 2)
        layout.addWidget(self.actButton7, 0, 3)
        layout.addWidget(self.actButton8, 1, 3)

        layout5 = Qt.QHBoxLayout()
        layout5.addWidget(self.startButton)
        layout5.addWidget(self.stopButton)

        self.frame5 = Qt.QFrame()
        self.frame5.setFrameStyle(1)

        frame_layout5 = Qt.QHBoxLayout()
        frame_layout5.addLayout(layout5)
        frame_layout5.addLayout(layout)
        self.frame5.setLayout(frame_layout5)

        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.frame5)
        layout1.addWidget(self.frame6)

        layout2 = Qt.QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.table)
        layout2.addWidget(label1)
        layout2.addWidget(self.txtEdt1)

        layout5 = Qt.QVBoxLayout()
        layout5.addWidget(self.canvas)
        layout5.addWidget(self.fig_statusbar)
        self.main_frame.setLayout(layout5)

        layout3 = Qt.QVBoxLayout()
        layout3.addWidget(self.frame4)
        layout3.addWidget(self.frame1)
        layout3.addWidget(self.frame2)
        layout3.addWidget(self.frame3)
        layout3.addStretch(True)

        layout4 = Qt.QHBoxLayout()
        layout4.addLayout(layout3)
        layout4.addLayout(layout2)
        
        self.setLayout(layout4)

        global global_results, vidTrack_setup_parameters, ard_setup_parameters, arena_setup_parameters, camera, video_name, recording, record_name
        global_results = {}
        vidTrack_setup_parameters = None
        ard_setup_parameters = None
        arena_setup_parameters = None
        camera = None
        video_name = None
        recording = False
        record_name = None

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        self.txtEdt1.append(text)

    def cell_was_clicked(self):
        global global_results
        try:
            current_row = self.table.currentRow()
            current_column = self.table.currentColumn()
            current_item_text = self.table.currentItem().text()
            if current_column == 5:
                global_results[str(current_row+1)]["trial_info"].update({"Comments":current_item_text})
        except:
            pass

    def new_edit_arena_setup(self):
        global arena_setup_parameters
        if arena_setup_parameters == None:
            try:
                from setup_arena_picture import arena_setup_parameters
            except:
                pass 
        self.new_edit_arena = setup_arena_picture.Window(cam=camera, vid_name=video_name, arena_sp=arena_setup_parameters)
        self.new_edit_arena.show()
        arena_setup_parameters = None

    def load_arena_setup(self):
        try:
            global arena_setup_parameters
            name = Qt.QFileDialog.getOpenFileName(self, 'Load Arena Setup')
            with open(name, 'r') as f:
                arena_setup_parameters = eval(f.read())
            print("loaded arena setup: %s" %(arena_setup_parameters))
        except:
            pass

    def save_arena_setup(self):
        global arena_setup_parameters
        try:
            try:
                from setup_arena_picture import arena_setup_parameters
            except:
                pass
            name = Qt.QFileDialog.getSaveFileName(self, 'Save Arena Setup')
            with open(name, 'w') as text_file:
                text_file.write(str(arena_setup_parameters))
            print("arena setup saved %s" %(arena_setup_parameters))
        except:
            pass
        
    def home(self):
        self.fig_toolbar.home()

    def pan(self):
        self.fig_toolbar.pan()

    def zoom_to_rect(self):
        self.fig_toolbar.zoom()

    def show_hide_labels(self):
        global arena_setup_parameters
        if self.lblsBtn.isChecked():
            # add labels to the grid squares
            self.grid_labels = []
            for j in range(self.num_height_divs):
                y = self.height_div/2+j*self.height_div
                for i in range(self.num_width_divs):
                    x = self.width_div/2.+float(i)*self.width_div
                    if arena_setup_parameters ['arena_pic_name'] != "no picture":
                        grid_label = self.axes.text(x,y, ("(%d,%d)" %(i,j)), fontsize=6, color='w', ha='center', va='center')
                    else:
                        grid_label = self.axes.text(x,y, ("(%d,%d)" %(i,j)), fontsize=6, color='b', ha='center', va='center')
                    self.grid_labels.append(grid_label)
                    self.canvas.draw()
        elif not self.lblsBtn.isChecked():
            for label in self.grid_labels:
                label.remove()
            self.canvas.draw()

    def redraw_arena_setup(self):
        global arena_setup_parameters
        
        if arena_setup_parameters == None:
            from setup_arena_picture import arena_setup_parameters

        self.lblsBtn.setChecked(False)
        
        self.arena_pic_name = arena_setup_parameters['arena_pic_name']
        try:
            self.arena_pic = mpimg.imread(self.arena_pic_name)
        except:
            pass
        self.arena_width = arena_setup_parameters['arena_width']
        self.arena_height = arena_setup_parameters['arena_height']
        self.width_div = arena_setup_parameters['width_div']
        self.height_div = arena_setup_parameters['height_div']
        self.num_width_divs = int(round(self.arena_width/self.width_div,0))
        self.num_height_divs = int(round(self.arena_height/self.height_div,0))

        self.fig.clear()
                
        self.axes = self.fig.add_subplot(111)
        try:
            self.axes.imshow(self.arena_pic, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        except:
            npArray = np.array([[[0, 0, 0, 0]]], dtype="uint8")
            self.axes.imshow(npArray, origin="lower", extent=(0,self.arena_width,0,self.arena_height))

        self.axes.set_xticks(np.arange(0, (self.arena_width+self.width_div),self.width_div))
        self.axes.set_yticks(np.arange(0, (self.arena_height+self.height_div),self.height_div))
        self.axes.tick_params(axis="both", which="major", labelsize="6")

        self.axes.grid(which="major", axis="both", linestyle='-', color='r')
        self.axes.xaxis.tick_top()
        self.axes.invert_yaxis()
        self.axes.set_xlabel("Arena Width (cm)", fontsize=8)
        self.axes.set_ylabel("Arena Height (cm)", fontsize=8)
        self.axes.tick_params(axis="both", which="major", labelsize=6)
        
        self.canvas.draw()

    def mouse_movement(self, event):
        try:
            self.coords_label.setText("x=%.3f,   y=%.3f" %(event.xdata, event.ydata))
        except:
            if not self.coords_label.text == "":
                self.coords_label.setText("")
            else:
                pass
       
    def connect_to_camera(self):
        global camera, vidTrack_setup_parameters
        if self.radBtn1.isChecked():
            try:
                camera = PiCamera()
                self.new_edit1.setDisabled(False)
                self.load1.setDisabled(False)
                self.save1.setDisabled(False)
                self.radBtn4.setDisabled(False)

                self.radBtn2.setChecked(False)
                #self.load_video_recording()
                
            except:
                print("Failed to connect to Camera")
                self.radBtn1.setChecked(False)  # change back to False

        elif not self.radBtn1.isChecked():
            try:
                camera.close()
                camera = None
            except:
                pass
            vidTrack_setup_parameters = None
            self.new_edit1.setDisabled(True)
            self.load1.setDisabled(True)
            self.save1.setDisabled(True)
            self.radBtn4.setDisabled(True)
            self.lneEdt1.setDisabled(True)

    def new_edit_video_tracking_method(self):
        global camera, video_name, vidTrack_setup_parameters
        if vidTrack_setup_parameters == None:
            try:
                from Camera_Wizard_v2 import vidTrack_setup_parameters
            except:
                pass
        self.cwiz = Camera_Wizard_v2.CameraWizard(cam = camera, vid_name = video_name, vidTrack_sp = vidTrack_setup_parameters)
        self.cwiz.show()
        vidTrack_setup_parameters = None

    def load_video_tracking_method(self):
        try:
            global vidTrack_setup_parameters
            name = Qt.QFileDialog.getOpenFileName(self, 'Load Video Tracking Method')
            with open(name, 'r') as f:
                vidTrack_setup_parameters = eval(f.read())
            print("loaded video tracking method: %s" %(vidTrack_setup_parameters))
        except:
            pass

    def save_video_tracking_method(self):
        global vidTrack_setup_parameters
        try:
            if vidTrack_setup_parameters == None:
                try:
                    from Camera_Wizard_v2 import vidTrack_setup_parameters
                except:
                    pass
            name = Qt.QFileDialog.getSaveFileName(self, 'Save Video Tracking Method')
            with open(name, 'w') as text_file:
                text_file.write(str(vidTrack_setup_parameters))
            print("video tracking method saved %s" %(vidTrack_setup_parameters))
        except:
            pass

    def video_record_trial(self):
        global recording, record_name
        if self.radBtn4.isChecked():
            self.lneEdt1.setDisabled(False)
            recording = True
            record_name = self.lneEdt1.text()
        elif not self.radBtn4.isChecked():
            self.lneEdt1.setDisabled(True)
            recording = False
            record_name = None
        
    def load_video_recording(self):
        global video_name, vidTrack_setup_parameters
        if self.radBtn2.isChecked():
            self.btnLneEdt1.setDisabled(False)
            self.radBtn4.setDisabled(False)

            self.radBtn1.setChecked(False)
            #self.connect_to_camera()

        elif not self.radBtn2.isChecked():
            video_name = None
            vidTrack_setup_parameters = None
            self.btnLneEdt1.clear()
            self.btnLneEdt1.setDisabled(True)
            self.new_edit2.setDisabled(True)
            self.load2.setDisabled(True)
            self.save2.setDisabled(True)
            
    def find_video_recording(self):
        try:
            global video_name
            video_name = Qt.QFileDialog.getOpenFileName(self, 'Find Video Recording')
            self.btnLneEdt1.setText(video_name)
            self.new_edit2.setDisabled(False)
            self.load2.setDisabled(False)
            self.save2.setDisabled(False)
            print("video name: %s" %(video_name))
        except:
            pass

    def connect_to_arduino(self):
        global a, ard_setup_parameters
        if self.radBtn3.isChecked():
            try:
                from nanpy import (SerialManager, ArduinoApi)
                connection = SerialManager()
                a = ArduinoApi(connection=connection)
                self.new_edit3.setDisabled(False)
                self.load3.setDisabled(False)
                self.save3.setDisabled(False)
            except:
                print("Failed to connect to Arduino")
                self.radBtn3.setChecked(False)   # change back to False
        elif not self.radBtn3.isChecked():
            try:
                del a
            except:
                pass
            ard_setup_parameters = None
            self.new_edit3.setDisabled(True)
            self.load3.setDisabled(True)
            self.save3.setDisabled(True)

    def new_edit_ard_method(self):
        global ard_setup_parameters
        if ard_setup_parameters == None:
            try:
                from Arduino_Wizard_v2 import ard_setup_parameters
            except:
                pass
        self.awiz = Arduino_Wizard_v2.ArduinoWizard(arduino_sp=ard_setup_parameters)
        self.awiz.show()
        ard_setup_parameters = None

    def load_ard_method(self):
        global ard_setup_parameters
        try:
            name = Qt.QFileDialog.getOpenFileName(self, 'Load Arduino Method')
            with open(name, 'r') as f:
                ard_setup_parameters = eval(f.read())
            print("loaded arduino method: %s" %(ard_setup_parameters))
        except:
            pass

    def save_ard_method(self):
        global ard_setup_parameters
        try:
            if ard_setup_parameters == None:
                try:
                    from Arduino_Wizard_v2 import ard_setup_parameters
                except:
                    pass
            name = Qt.QFileDialog.getSaveFileName(self, 'Save Arduino Method')
            with open(name, 'w') as text_file:
                text_file.write(str(ard_setup_parameters))
            print("arduino method saved %s" %(ard_setup_parameters))
        except:
            pass
    
    def timer_start(self):
        global s,m,h
         
        self.timer.start(1000)
     
    def timer_time(self):
        global s,m,h
 
        if s < 59:
            s += 1
        else:
            if m < 59:
                s = 0
                m += 1
            elif m == 59 and h < 24:
                h += 1
                m = 0
                s = 0
            else:
                self.timer.stop()
 
        time = "{0}:{1}:{2}".format(h,m,s)
 
        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)
        self.activateWindow()

    def timer_reset(self):
        global s,m,h
 
        self.timer.stop()
 
        s = 0
        m = 0
        h = 0
 
        time = "{0}:{1}:{2}".format(h,m,s)
 
        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)

    def start_pressed(self):
        global global_results, ard_results, _isRunning2, vidTrack_setup_parameters, ard_setup_parameters
        
        date = strftime("%Y-%m-%d")
        start_time = strftime("%H:%M:%S")

        self.timer_reset()
        self.timer_start()
        
        trck = self.vidTracking.Run()

        while _isRunning2:
            Qt.qApp.processEvents()
            continue

        self.timer.stop()
        
        end_time = strftime("%H:%M:%S")

        self.actButton1.setChecked(False)
        self.actButton2.setChecked(False)
        self.actButton3.setChecked(False)
        self.actButton4.setChecked(False)
        self.actButton5.setChecked(False)
        self.actButton6.setChecked(False)
        self.actButton7.setChecked(False)
        self.actButton8.setChecked(False)

        vidTrack_results = {}
        try:
            if (vidTrack_setup_parameters['video_tracking_algorithm'] == "Frame Differencing") or (vidTrack_setup_parameters['video_tracking_algorithm'] == "MOG") :
                vidTrack_results['vid_time'] = trck[0]
                vidTrack_results['position'] = trck[1]
            elif vidTrack_setup_parameters['video_tracking_algorithm'] == "None":
                vidTrack_results['vid_time'] = trck
        except:
            pass
        
        try:
            try:
                duration = str(vidTrack_results['vid_time'][-1])
            except:
                duration = str(ard_results['ard_loop_time'][-1])
        except:
            duration = str(0)

        trial_info = {"Date":date, "Start_Time":start_time, "End_Time":end_time, "Trial_Duration":duration}

        self.table_rowCount += 1
        self.table.setRowCount(self.table_rowCount)

        global_results[str(self.table_rowCount)] = {}
        global_results[str(self.table_rowCount)]["trial_info"] = trial_info
        global_results[str(self.table_rowCount)]["results"] = vidTrack_results
        global_results[str(self.table_rowCount)]["results"].update(ard_results)
            
        self.table.setItem(self.table_rowCount-1, 0, Qt.QTableWidgetItem(str(self.table_rowCount)))
        self.table.setItem(self.table_rowCount-1, 1, Qt.QTableWidgetItem(date))
        self.table.setItem(self.table_rowCount-1, 2, Qt.QTableWidgetItem(start_time))
        self.table.setItem(self.table_rowCount-1, 3, Qt.QTableWidgetItem(end_time))
        self.table.setItem(self.table_rowCount-1, 4, Qt.QTableWidgetItem(duration))


# main ============================================
     
def main():
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())    

if __name__ == '__main__':
    main()
