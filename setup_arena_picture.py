# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from vid_tracking_methods import (live_cap_arena_pic, vid_cap_arena_pic)

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

class Window(Qt.QWidget):
    def __init__(self, cam, vid_name, arena_sp):
        Qt.QWidget.__init__(self)

        self.cam = cam
        self.vid_name = vid_name

        global arena_setup_parameters
        arena_setup_parameters = arena_sp

        boldFont = Qt.QFont()
        boldFont.setBold(True)

        lbl1 = Qt.QLabel(self.tr("Load Arena Picture:"))
        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.buttonClicked.connect(self.find_arena_pic)
        lbl1.setBuddy(self.btnLneEdt1)
        try:
            if arena_setup_parameters['arena_pic_name'] != "no picture":
                self.btnLneEdt1.setText(arena_setup_parameters['arena_pic_name'])
        except:
            pass

        lbl2 = Qt.QLabel(self.tr("OR"))
        lbl2.setFont(boldFont)

        lbl3 = Qt.QLabel(self.tr("Capture Reference Image:"))
        self.lneEdt1 = Qt.QLineEdit()
        self.lneEdt1.setText("example_arena_pic.png")
        lbl3.setBuddy(self.lneEdt1)
        if (self.cam==None) and (self.vid_name==None):
            self.lneEdt1.setDisabled(True)
        
        self.pshBtn1 = Qt.QPushButton(self.tr("Capture"))
        self.pshBtn1.clicked.connect(self.capture_arena_pic)
        if (self.cam==None) and (self.vid_name==None):
            self.pshBtn1.setDisabled(True)
        
        lbl4 = Qt.QLabel("Arena Width (cm):")
        self.lneEdt2 = Qt.QLineEdit()
        lbl4.setBuddy(self.lneEdt2)
        try:
            self.lneEdt2.setText(str(arena_setup_parameters['arena_width']))
        except:
            pass

        lbl5 = Qt.QLabel("Arena Height (cm):")
        self.lneEdt3 = Qt.QLineEdit()
        lbl5.setBuddy(self.lneEdt3)
        try:
            self.lneEdt3.setText(str(arena_setup_parameters["arena_height"]))
        except:
            pass

        lbl6 = Qt.QLabel("Number of vertical lines dividing arena:")
        self.spnBox1 = Qt.QSpinBox()
        lbl6.setBuddy(self.spnBox1)
        try:
            num_width_divs = round((int(arena_setup_parameters["arena_width"])/int(arena_setup_parameters["width_div"])),0)-1
            self.spnBox1.setValue(num_width_divs)
        except:
            pass

        lbl7 = Qt.QLabel("Number of horizontal lines dividing arena:")
        self.spnBox2 = Qt.QSpinBox()
        lbl7.setBuddy(self.spnBox2)
        try:
            num_height_divs = round((int(arena_setup_parameters["arena_height"])/int(arena_setup_parameters["height_div"])),0)-1
            self.spnBox2.setValue(num_height_divs)
        except:
            pass

        self.radBtn1 = Qt.QRadioButton(self.tr("Show grid labels in arena setup preview (OPTIONAL)"))
        self.radBtn1.setChecked(False)

        self.pshBtn2 = Qt.QPushButton(self.tr("&Preview Arena Setup"))
        self.pshBtn2.clicked.connect(self.draw_arena_setup)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()

        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.lneEdt1)
        layout1.addWidget(self.pshBtn1)

        layout2 = Qt.QFormLayout()
        layout2.addRow(lbl1, self.btnLneEdt1)
        layout2.addRow(lbl2)
        layout2.addRow(lbl3, layout1)

        layout3 = Qt.QFormLayout()
        layout3.addRow(lbl4, self.lneEdt2)
        layout3.addRow(lbl5, self.lneEdt3)
        layout3.addRow(lbl6, self.spnBox1)
        layout3.addRow(lbl7, self.spnBox2)

        layout4 = Qt.QVBoxLayout()
        layout4.addLayout(layout2)
        layout4.addWidget(spacer1)
        layout4.addLayout(layout3)
        layout4.addWidget(spacer2)
        layout4.addWidget(self.radBtn1)
        layout4.addWidget(spacer3)
        layout4.addWidget(self.pshBtn2)

        self.setLayout(layout4)

        self.setMinimumWidth(450)

    def find_arena_pic(self):
        try:
            self.arena_pic_name = Qt.QFileDialog.getOpenFileName(self, 'Load Picture of Arena')
            self.btnLneEdt1.setText(self.arena_pic_name)
        except:
            pass

    def capture_arena_pic(self):
        self.arena_pic_name = self.lneEdt1.text()
        if self.cam != None:
            temp_image = live_cap_arena_pic(self.cam, self.arena_pic_name)
        elif self.vid_name != None:
            temp_image = vid_cap_arena_pic(self.vid_name, self.arena_pic_name)
        
    def draw_arena_setup(self):
        global arena_setup_parameters
        self.arena_pic_name = self.btnLneEdt1.text()
        try:
            self.arena_pic = mpimg.imread(self.arena_pic_name)
            arena_setup_parameters = {"arena_pic_name":self.arena_pic_name}
        except:
            arena_setup_parameters = {"arena_pic_name":"no picture"}
        self.arena_width = float(self.lneEdt2.text())
        self.arena_height = float(self.lneEdt3.text())
        self.num_width_divs = int(self.spnBox1.text())+1
        self.num_height_divs = int(self.spnBox2.text())+1
        self.width_div = self.arena_width/self.num_width_divs
        self.height_div = self.arena_height/self.num_height_divs

        arena_setup_parameters["arena_width"] = self.arena_width
        arena_setup_parameters["arena_height"] = self.arena_height
        arena_setup_parameters["width_div"] = self.width_div
        arena_setup_parameters["height_div"] = self.height_div

        self.fig = plt.figure()
        self.fig.canvas.set_window_title("Arena Setup Preview")

        self.fig.clear()
                
        self.axes = self.fig.add_subplot(111)
        try:
            self.axes.imshow(self.arena_pic, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        except:
            npArray = np.array([[[0, 0, 0, 0]]], dtype="uint8")
            self.axes.imshow(npArray, origin="lower", extent=(0,self.arena_width,0,self.arena_height))

        self.axes.set_xticks(np.arange(0, (self.arena_width+self.width_div),self.width_div))
        self.axes.set_yticks(np.arange(0, (self.arena_height+self.height_div),self.height_div))
                             
        self.axes.grid(which="major", axis="both", linestyle='-', color='r')
        self.axes.xaxis.tick_top()
        self.axes.invert_yaxis()
        self.axes.set_xlabel("Arena Width (cm)", fontsize=12)
        self.axes.set_ylabel("Arena Height (cm)", fontsize=12)
        self.axes.tick_params(axis="both", which="major", labelsize=10)

        if self.radBtn1.isChecked():
            # add labels to the grid squares
            for j in range(self.num_height_divs):
                y = self.height_div/2+j*self.height_div
                for i in range(self.num_width_divs):
                    x = self.width_div/2.+float(i)*self.width_div
                    if arena_setup_parameters ['arena_pic_name'] != "no picture":
                        grid_label = self.axes.text(x,y, ("(%d,%d)" %(i,j)), fontsize=10, color='w', ha='center', va='center')
                    else:
                        grid_label = self.axes.text(x,y, ("(%d,%d)" %(i,j)), fontsize=10, color='b', ha='center', va='center')

        plt.show()
   

# main ===============================================

def main():
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
