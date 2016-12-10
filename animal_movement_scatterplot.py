# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:58:14 2016

@author: Matt
"""

from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
import numpy as np
import sys

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

class Scatter(Qt.QWidget):
    def __init__(self, parent=None):
        super(Scatter, self).__init__(parent)
        
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

        lbl3 = Qt.QLabel("Number of vertical lines dividing arena:")
        self.spnBox1 = Qt.QSpinBox()
        lbl3.setBuddy(self.spnBox1)

        lbl4 = Qt.QLabel("Number of horizontal lines dividing arena:")
        self.spnBox2 = Qt.QSpinBox()
        lbl4.setBuddy(self.spnBox2)
                
        self.radBtn1 = Qt.QRadioButton(self.tr("Load arena picture for scatterplot background (OPTIONAL)"))
        self.radBtn1.setChecked(False)  
        self.radBtn1.clicked.connect(self.use_arena_pic)

        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.buttonClicked.connect(self.find_arena_pic)
        self.btnLneEdt1.setDisabled(True)

        self.pshBtn1 = Qt.QPushButton('Draw Scatterplot', self)
        self.pshBtn1.clicked.connect(self.draw_scatterplot)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()

        layout1 = Qt.QFormLayout()
        layout1.addRow(lbl1, self.lneEdt1)
        layout1.addRow(lbl2, self.lneEdt2)
        layout1.addRow(lbl3, self.spnBox1)
        layout1.addRow(lbl4, self.spnBox2)
   
        layout2 = Qt.QVBoxLayout(self)
        layout2.addWidget(self.cmBox1)
        layout2.addWidget(spacer1)
        layout2.addLayout(layout1)
        layout2.addWidget(spacer2)
        layout2.addWidget(self.radBtn1)
        layout2.addWidget(self.btnLneEdt1)
        layout2.addWidget(spacer3)
        layout2.addWidget(self.pshBtn1)

        self.setWindowTitle(self.tr("Animal Movement Scatterplot"))

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

    def draw_scatterplot(self):
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
        self.num_width_divs = int(self.spnBox1.text())+1
        self.num_height_divs = int(self.spnBox2.text())+1
        self.width_div = self.arena_width/self.num_width_divs
        self.height_div = self.arena_height/self.num_height_divs

        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Scatterplot" %(self.cmBox1.currentText()))
        l, = plt.plot(self.posx, self.posy, marker='.', linestyle='-')
        plt.xlim(0, self.arena_width)
        plt.ylim(0, self.arena_height)
        plt.gca().xaxis.tick_top()
        plt.gca().invert_yaxis()
        plt.gca().set_aspect("equal")

        plt.gca().set_xticks(np.arange(0, (self.arena_width+self.width_div),self.width_div))
        plt.gca().set_yticks(np.arange(0, (self.arena_height+self.height_div),self.height_div))
        plt.gca().grid(which="major", axis="both", linestyle='-', color='r')
        
        try:
            self.arena_pic_name = self.btnLneEdt1.text()
            self.arena_pic = mpimg.imread(self.arena_pic_name)
            plt.gca().imshow(self.arena_pic, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        except:
            pass

        plt.xlabel("Arena Width (cm)")
        plt.ylabel("Arena Height (cm)")

        axcolour = 'lightgoldenrodyellow'
        axtime = plt.axes([0.25, 0.025, 0.65, 0.03], axisbg = axcolour)

        end_time = self.time[-1]

        stime = Slider(axtime, 'Time', 0, end_time, valinit = end_time)

        def update(val):
            time = stime.val
            for i in range(len(self.time)+1):
                try:
                    if self.time[i] <= time < self.time[i+1]:
                        l.set_xdata(self.posx[:i])
                        l.set_ydata(self.posy[:i])
                        plt.draw
                except:
                    pass
        stime.on_changed(update)
        plt.show()


# main ===========================================

def main():
    app = Qt.QApplication(sys.argv)
    scatter = Scatter()
    plot.show()
    
    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()
