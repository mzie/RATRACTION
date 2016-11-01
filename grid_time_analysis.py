from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
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

        lbl1 = Qt.QLabel("Arena Width (cm):")
        self.lneEdt1 = Qt.QLineEdit()
        lbl1.setBuddy(self.lneEdt1)

        lbl2 = Qt.QLabel("Arena Height (cm):")
        self.lneEdt2 = Qt.QLineEdit()
        lbl2.setBuddy(self.lneEdt2)

        lbl3 = Qt.QLabel("Number of vertical lines dividing arena:")
        self.spnBox1 = Qt.QSpinBox()
        lbl3.setBuddy(self.spnBox1)

        lbl4 = Qt.QLabel("Number of horizontal lines dividing arena:")
        self.spnBox2 = Qt.QSpinBox()
        lbl4.setBuddy(self.spnBox2)

        self.radBtn1 = Qt.QRadioButton(self.tr("Load arena picture for arena setup subplot background (OPTIONAL)"))
        self.radBtn1.setChecked(False)  
        self.radBtn1.clicked.connect(self.use_arena_pic)

        self.btnLneEdt1 = ButtonLineEdit()
        self.btnLneEdt1.buttonClicked.connect(self.find_arena_pic)
        self.btnLneEdt1.setDisabled(True)

        self.pshBtn1 = Qt.QPushButton(self.tr('Draw ROI Time Bar Graph'))
        self.pshBtn1.clicked.connect(self.draw_bar_graph)

        self.pshBtn1 = Qt.QPushButton(self.tr('Draw Grid Time Bar Graph'))
        self.pshBtn1.clicked.connect(self.draw_bar_graph)

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

        self.setWindowTitle(self.tr("Grid Time Analysis"))

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

    def calc_grid(self):
        self.arena_width = float(self.lneEdt1.text())
        self.arena_height = float(self.lneEdt2.text())
        self.num_width_divs = int(self.spnBox1.text())+1
        self.num_height_divs = int(self.spnBox2.text())+1
        self.width_div = self.arena_width/self.num_width_divs
        self.height_div = self.arena_height/self.num_height_divs
        
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']

        section = [(x,y) for y in range(self.num_height_divs)
                   for x in range(self.num_width_divs)]
        grid = OrderedDict()
        for gridy in section:
                   grid[gridy] = [(gridy[0]*self.width_div, gridy[1]*self.height_div),
                                  ((gridy[0]+1)*self.width_div, (gridy[1]+1)*self.height_div), 0]
        time_ints = [(time[i+1]-time[i]) for i in range(len(time)-1)]
        for tim, pos in zip(time_ints, pos):
            for key in grid:
                if (grid[key][0][0] <= pos[0] < grid[key][1][0]) and (grid[key][0][1] <= pos[1] <= grid[key][1][1]):
                    grid[key][2] += tim
        for key in grid.keys():
            grid[key][2] = round(grid[key][2],2)
        return grid

    def draw_bar_graph(self):
        grid = self.calc_grid()
        fig = plt.gcf()
        fig.canvas.set_window_title("Trial %s Time Spent in Arena Grids" %(self.cmBox1.currentText()))
        ax1 = plt.subplot(121)
        positions = []
        values = []
        LABELS = []
        count = 0
        for key in grid.keys():
            if grid[key][2] > 0:
                positions.append(count)
                values.append(grid[key][2])
                LABELS.append(str(key))
                count += 1
        ax1.barh(positions, values, align="center")
        locs, labels = plt.yticks(positions, LABELS)
        plt.xlabel("Time Spent in Grid (seconds)")
        plt.ylabel("Arena Grids")

        self.arena_pic_name = self.btnLneEdt1.text()
        try:
            self.arena_pic = mpimg.imread(self.arena_pic_name)
        except:
            pass

        ax2 = plt.subplot(122)
        try:
            ax2.imshow(self.arena_pic, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        except:
            npArray = np.array([[[0, 0, 0, 0]]], dtype="uint8")
            ax2.imshow(npArray, origin="lower", extent=(0,self.arena_width,0,self.arena_height))
        
        ax2.set_xticks(np.arange(0, (self.arena_width+self.width_div),self.width_div))
        ax2.set_yticks(np.arange(0, (self.arena_height+self.height_div),self.height_div))
                             
        ax2.grid(which="major", axis="both", linestyle='-', color='r')
        ax2.xaxis.tick_top()
        ax2.invert_yaxis()
        ax2.set_xlabel("Arena Width (cm)", fontsize=12)
        ax2.set_ylabel("Arena Height (cm)", fontsize=12)
        ax2.tick_params(axis="both", which="major", labelsize=10)

        # add labels to the grid squares
        for j in range(self.num_height_divs):
            y = self.height_div/2+j*self.height_div
            for i in range(self.num_width_divs):
                x = self.width_div/2.+float(i)*self.width_div
                if self.radBtn1.isChecked():
                    ax2.text(x,y, ("(%d,%d)" %(i,j)), color='w', ha='center', va='center')
                elif not self.radBtn1.isChecked():
                    ax2.text(x,y, ("(%d,%d)" %(i,j)), color='b', ha='center', va='center')

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
