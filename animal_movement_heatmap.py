from PyQt4 import Qt
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
import sys
import csv

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

        lbl3 = Qt.QLabel("Number of vertical lines dividing arena:")
        self.spnBox1 = Qt.QSpinBox()
        lbl3.setBuddy(self.spnBox1)

        lbl4 = Qt.QLabel("Number of horizontal lines dividing arena:")
        self.spnBox2 = Qt.QSpinBox()
        lbl4.setBuddy(self.spnBox2)

        lbl5 = Qt.QLabel("Interpolation Method:")
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItems(["none", "nearest", "bilinear", "bicubic", "spline16",
                              "spline36", "hanning", "hamming", "hermite", "kaiser",
                              "quadric", "catrom", "gaussian", "bessel", "mitchell",
                              "sinc", "lanczos"])
        lbl5.setBuddy(self.cmBox2)
        
        self.pshBtn1 = Qt.QPushButton(self.tr('Draw Grid Time Heatmap'))
        self.pshBtn1.clicked.connect(self.draw_heatmap)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        spacer3 = Qt.QLabel()

        layout1 = Qt.QFormLayout()
        layout1.addRow(lbl1, self.lneEdt1)
        layout1.addRow(lbl2, self.lneEdt2)
        layout1.addRow(lbl3, self.spnBox1)
        layout1.addRow(lbl4, self.spnBox2)

        layout2 = Qt.QFormLayout()
        layout2.addRow(lbl5, self.cmBox2)

        layout3 = Qt.QVBoxLayout(self)
        layout3.addWidget(self.cmBox1)
        layout3.addWidget(spacer1)
        layout3.addLayout(layout1)
        layout3.addWidget(spacer2)
        layout3.addLayout(layout2)
        layout3.addWidget(spacer3)
        layout3.addWidget(self.pshBtn1)

        self.setWindowTitle(self.tr("Animal Movement Heatmap"))

    def calc_grid(self):
        self.arena_width = float(self.lneEdt1.text())
        self.arena_height = float(self.lneEdt2.text())
        self.num_width_divs = int(self.spnBox1.text())+1
        self.num_height_divs = int(self.spnBox2.text())+1
        self.width_div = self.arena_width/self.num_width_divs
        self.height_div = self.arena_height/self.num_height_divs
        
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_pts_time']]
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

    def draw_heatmap(self):
        interpolation_method = self.cmBox2.currentText()
        grid = self.calc_grid()
        x = []
        y = []
        times = []
        for key in grid.keys():
            x.append(((grid[key][0][0]+grid[key][1][0])/2))
            y.append(((grid[key][0][1]+grid[key][1][1])/2))
            times.append(grid[key][2])
                       
        xedges = list(np.arange(0, (self.arena_width+self.width_div),self.width_div))
        yedges = list(np.arange(0, (self.arena_height+self.height_div),self.height_div))
        # not sure why y and x needed to be swapped but they did for it to work :\
        h, _, _, _ = plt.hist2d(y, x, bins=[yedges, xedges], weights=times)
        plt.clf()
        plt.close()
        fig = plt.gcf()
        fig.canvas.set_window_title("Trial %s Heatmap" %(self.cmBox1.currentText()))
        plt.imshow(h,interpolation=interpolation_method, aspect="auto", origin="lower", extent=[0,self.arena_width,0,self.arena_height])
        plt.gca().xaxis.tick_top()
        plt.gca().invert_yaxis()
        plt.gca().set_aspect("equal")
        plt.xlabel("Arena Width (cm)")
        plt.ylabel("Arena Height (cm)")
        plt.colorbar(label="Time spent in grid (seconds)")
        plt.show()


# main ================================================

def main():
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()
        
