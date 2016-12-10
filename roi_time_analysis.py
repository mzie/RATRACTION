import sys
from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
from collections import OrderedDict

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
    def __init__(self):
        Qt.QWidget.__init__(self)

        global global_results
        from OneStopTrack import global_results

        self.cmBox1 = Qt.QComboBox()
        for key in global_results.keys():
            self.cmBox1.addItem(str(key))

        lbl1 = Qt.QLabel("Arena width (cm):")
        self.lneEdt1 = Qt.QLineEdit()
        lbl1.setBuddy(self.lneEdt1)

        lbl2 = Qt.QLabel("Arena height (cm):")
        self.lneEdt2 = Qt.QLineEdit()
        lbl2.setBuddy(self.lneEdt2)

        lbl3 = Qt.QLabel("Region of Interest (ROI) is the")
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItems(["area inside of the rectangle", "area outside of the rectangle"])
        lbl3.setBuddy(self.cmBox2)

        lbl4 = Qt.QLabel("Rectangle Top Left Corner X Coordinate (cm):")
        self.lneEdt3 = Qt.QLineEdit()
        lbl4.setBuddy(self.lneEdt3)

        lbl5 = Qt.QLabel("Rectangle Top Left Corner Y Coordinate (cm):")
        self.lneEdt4 = Qt.QLineEdit()
        lbl5.setBuddy(self.lneEdt4)

        lbl6 = Qt.QLabel("Rectangle Bottom Right Corner X Coordinate (cm):")
        self.lneEdt5 = Qt.QLineEdit()
        lbl6.setBuddy(self.lneEdt5)

        lbl7 = Qt.QLabel("Rectangle Bottom Right Corner Y Coordinate (cm):")
        self.lneEdt6 = Qt.QLineEdit()
        lbl7.setBuddy(self.lneEdt6)

        self.radBtn1 = Qt.QRadioButton(self.tr("Load arena picture for arena setup subplot background (OPTIONAL)"))
        self.radBtn1.setChecked(False)  
        self.radBtn1.clicked.connect(self.use_arena_pic)

        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.buttonClicked.connect(self.find_arena_pic)
        self.btnLneEdt1.setDisabled(True)

        self.pshBtn1 = Qt.QPushButton(self.tr('Draw ROI Time Bar Graph'))
        self.pshBtn1.clicked.connect(self.draw_bar_graph)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()
        spacer4 = Qt.QLabel()

        layout1 = Qt.QFormLayout()
        layout1.addRow(lbl1, self.lneEdt1)
        layout1.addRow(lbl2, self.lneEdt2)

        layout2 = Qt.QFormLayout()
        layout2.addRow(lbl3, self.cmBox2)

        layout3 = Qt.QFormLayout()
        layout3.addRow(lbl4, self.lneEdt3)
        layout3.addRow(lbl5, self.lneEdt4)
        layout3.addRow(lbl6, self.lneEdt5)
        layout3.addRow(lbl7, self.lneEdt6)

        layout4 = Qt.QVBoxLayout(self)
        layout4.addWidget(self.cmBox1)
        layout4.addWidget(spacer1)
        layout4.addLayout(layout1)
        layout4.addWidget(spacer2)
        layout4.addLayout(layout2)
        layout4.addLayout(layout3)
        layout4.addWidget(spacer3)
        layout4.addWidget(self.radBtn1)
        layout4.addWidget(self.btnLneEdt1)
        layout4.addWidget(spacer4)
        layout4.addWidget(self.pshBtn1)

        self.setWindowTitle(self.tr("ROI Time Analysis"))

    def use_arena_pic(self):
        if self.radBtn1.isChecked():
            self.btnLneEdt1.setDisabled(False)
        elif not self.radBtn1.isChecked():
            self.btnLneEdt1.clear()
            self.btnLneEdt1.setDisabled(True)

    def find_arena_pic(self):
        try:
            self.arena_pic_name = Qt.QFileDialog.getOpenFileName(self, 'Load Picture of Arena')
            self.btnLneEdt1.setText(self.arena_pic_name)
        except:
            pass

    def calc_roi(self):
        self.posx = []
        self.posy = []
        self.time = []
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_pts_time']]
        try:
            position = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            position = global_results[str(self.cmBox1.currentText())]["results"]['position']
        for tim, pos in zip(time, position):
            self.posx.append(pos[0])
            self.posy.append(pos[1])
            self.time.append(tim)

        self.arena_width = float(self.lneEdt1.text())
        self.arena_height = float(self.lneEdt2.text())

        self.roi_tl_x = float(self.lneEdt3.text())
        self.roi_tl_y = float(self.lneEdt4.text())
        self.roi_br_x = float(self.lneEdt5.text())
        self.roi_br_y = float(self.lneEdt6.text())

        self.time_ints = np.diff(self.time)

        self.time_in_roi = 0
        self.time_out_roi = 0

        roi = OrderedDict()

        if self.cmBox2.currentText() == "area inside of the rectangle":
            for time_int,x,y in zip(self.time_ints,self.posx, self.posy):
                if (((x >= self.roi_tl_x) and (y >= self.roi_tl_y)) and ((x <= self.roi_br_x) and (y <= self.roi_br_y))):
                    self.time_in_roi += time_int
                else:
                    self.time_out_roi += time_int
        elif self.cmBox2.currentText() == "area outside of the rectangle":
            for time_int,x,y in zip(self.time_ints,self.posx, self.posy):
                if (((x <= self.roi_tl_x) or (x >= self.roi_br_x)) or ((y <= self.roi_tl_y) or (y >= self.roi_br_y))):
                    self.time_in_roi += time_int
                else:
                    self.time_out_roi += time_int
        roi["ROI"] = self.time_in_roi
        roi["Not ROI"] = self.time_out_roi
        return roi

    def draw_bar_graph(self):
        roi = self.calc_roi()
        fig = plt.gcf()
        fig.canvas.set_window_title("Trial %s Time Spent in Region of Interest" %(self.cmBox1.currentText()))
        ax1 = plt.subplot(121)
        positions = [0 ,1]
        values = [roi[key] for key in roi.keys()]
        LABELS = ["ROI", "Not ROI"]
        bars = ax1.barh(positions, values, height=0.1, align="center")
        bars[0].set_color('r')
        locs, labels = plt.yticks(positions, LABELS)
        plt.xlabel("Time Spent in Arena Location (seconds)")

        ax2 = plt.subplot(122)
        self.arena_pic_name = self.btnLneEdt1.text()
        try:
            self.arena_pic = mpimg.imread(self.arena_pic_name)
        except:
            pass
        try:
            ax2.imshow(self.arena_pic, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        except:
            npArray = np.array([[[0, 0, 0, 0]]], dtype="uint8")
            ax2.imshow(npArray, origin="lower", extent=(0,self.arena_width,0,self.arena_height))

        ax2.xaxis.tick_top()
        ax2.invert_yaxis()
        ax2.set_xlabel("Arena Width (cm)", fontsize=12)
        ax2.set_ylabel("Arena Height (cm)", fontsize=12)
        ax2.tick_params(axis="both", which="major", labelsize="10")

        # draw ROI and not ROI areas
        if self.cmBox2.currentText() == "area inside of the rectangle":
            if self.radBtn1.isChecked():
                ax2.add_patch(patches.Rectangle((0, 0), self.arena_width, self.arena_height, alpha=0.6))
                ax2.add_patch(patches.Rectangle((self.roi_tl_x, self.roi_tl_y), (self.roi_br_x - self.roi_tl_x), (self.roi_br_y - self.roi_tl_y), facecolor="red", alpha=0.6))
            elif not self.radBtn1.isChecked():
                ax2.add_patch(patches.Rectangle((0, 0), self.arena_width, self.arena_height))
                ax2.add_patch(patches.Rectangle((self.roi_tl_x, self.roi_tl_y), (self.roi_br_x - self.roi_tl_x), (self.roi_br_y - self.roi_tl_y), facecolor="red"))
        elif self.cmBox2.currentText() == "area outside of the rectangle":
            if self.radBtn1.isChecked():
                ax2.add_patch(patches.Rectangle((0, 0), self.arena_width, self.arena_height, facecolor="red", alpha=0.6))
                ax2.add_patch(patches.Rectangle((self.roi_tl_x, self.roi_tl_y), (self.roi_br_x - self.roi_tl_x), (self.roi_br_y - self.roi_tl_y), alpha=0.6))
            elif not self.radBtn1.isChecked():
                ax2.add_patch(patches.Rectangle((0, 0), self.arena_width, self.arena_height, facecolor="red"))
                ax2.add_patch(patches.Rectangle((self.roi_tl_x, self.roi_tl_y), (self.roi_br_x - self.roi_tl_x), (self.roi_br_y - self.roi_tl_y)))

        plt.tight_layout()
        plt.show()


# main =================================================
               
def main():    
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()

        
