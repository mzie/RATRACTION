# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 14:29:45 2016

@author: Matt
"""

from PyQt4 import Qt
from collections import deque
import matplotlib.pyplot as plt
import itertools
import sys

class Window(Qt.QWidget):
    def __init__(self):
        Qt.QWidget.__init__(self)
        
        global global_results
        from OneStopTrack import global_results

        self.cmBox1 = Qt.QComboBox()

        for key in global_results.keys():
            self.cmBox1.addItem(str(key))
        
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItems(["Total_Distance_Travelled", "Linear_Distance_Travelled",
                              "Horizontal_Distance_Travelled", "Vertical_Distance_Travelled",
                              "Average_Velocity"])
        
        self.pshBtn1 = Qt.QPushButton('Graph Locomotor Parameter', self)
        self.pshBtn1.clicked.connect(self.handleButton1)

        spacer1 = Qt.QLabel()
        spacer2 = Qt.QLabel()
        
        layout1 = Qt.QVBoxLayout(self)
        layout1.addWidget(self.cmBox1)
        layout1.addWidget(spacer1)
        layout1.addWidget(self.cmBox2)
        layout1.addWidget(spacer2)
        layout1.addWidget(self.pshBtn1)

        self.setWindowTitle(self.tr("Locomotor Parameters"))

    def handleButton1(self):
        exec('self.%s()' %(self.cmBox2.currentText()))

    def Linear_Distance_Travelled(self):
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']

        linear_distance = [(((pos[i+1][0]-pos[i][0])**2+(
            pos[i+1][1]-pos[i][1])**2))**0.5 for i in range(len(pos)-1)]

        plot_time = deque(itertools.islice(time, 1, len(time)))

        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Linear Distance Travelled" %(self.cmBox1.currentText()))
        plt.plot(plot_time, linear_distance, marker='.', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Linear Distance Travelled (cm)")
        plt.show()

    def Total_Distance_Travelled(self):
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']

        linear_distance = [(((pos[i+1][0]-pos[i][0])**2+(
            pos[i+1][1]-pos[i][1])**2))**0.5 for i in range(len(pos)-1)]
        
        from itertools import accumulate

        total_distance = [0] + list(accumulate(linear_distance))

        plot_time = deque(itertools.islice(time, 1, len(time)))
        plot_time.appendleft(0)
        
        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Total Distance Travelled" %(self.cmBox1.currentText()))
        plt.plot(plot_time, total_distance, marker='.', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Total Distance Travelled (cm)")
        plt.show()

    def Horizontal_Distance_Travelled(self):
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']

        horizontal_distance = [pos[i][0] for i in range(len(pos)-1)]

        plot_time = deque(itertools.islice(time, 1, len(time)))

        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Horizontal Distance Travelled" %(self.cmBox1.currentText()))
        plt.plot(plot_time, horizontal_distance, marker='.', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Horizontal Distance Travelled (cm)")
        plt.show()

    def Vertical_Distance_Travelled(self):
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']

        vertical_distance = [pos[i][1] for i in range(len(pos)-1)]

        plot_time = deque(itertools.islice(time, 1, len(time)))

        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Vertical Distance Travelled" %(self.cmBox1.currentText()))
        plt.plot(plot_time, vertical_distance, marker='.', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Vertical Distance Travelled (cm)")
        plt.show()

    def Total_Time_Spent_Moving_and_Stationary(self):
        pass
##        time = [float(tim) for tim in global_results[str(self.cmBox.currentText())]['vid_time']]
##        try:
##            pos = [eval(posi) for posi in global_results[str(self.cmBox.currentText())]['position']]
##        except:
##            pos = global_results[str(self.cmBox.currentText())]['position']
##        
##        linear_distance = [(((pos[i+1][0]-pos[i][0])**2+(
##            pos[i+1][1]-pos[i][1])**2))**0.5 for i in range(len(pos)-1)]
##
##        time_ints = [(time[i+1]-time[i]) for i in range(len(time)-1)]
##
##        time_tracker = 0
##        linear_distance_tracker = 0
##
##        time_moving = 0
##        time_stationary = 0
##
##        for distance, time_int in zip(linear_distance, time_ints):
##            time_tracker += time_int
##            linear_distance_tracker += distance
##            if time_tracker > 0.5:
##                if linear_distance_tracker > 5:
##                    time_moving += time_tracker
##                    time_tracker = 0
##                elif linear_distance_tracker < 5:
##                    time_stationary += time_tracker
##                    time_tracker = 0
##
##
##        ax = plt.subplot(111)
##        xticks  = [0, 1]
##        ax.bar(0, time_moving, width=0.3, color='g', align='center')
##        ax.bar(1, time_stationary, width=0.3, color='b', align='center')
##        LABELS = ["Moving", "Stationary"]
##        plt.xticks(xticks, LABELS)
##        plt.ylabel("Time (s)")
##        plt.show()

    def Average_Velocity(self):
        time = [float(tim) for tim in global_results[str(self.cmBox1.currentText())]["results"]['vid_time']]
        try:
            pos = [eval(posi) for posi in global_results[str(self.cmBox1.currentText())]["results"]['position']]
        except:
            pos = global_results[str(self.cmBox1.currentText())]["results"]['position']
        linear_distance = []
        for i in range(len(pos)):
            try:
                linear_distance.append((((pos[i+1][0]-pos[i][0])**2+(pos[i+1][1]-pos[i][1])**2))**0.5)
            except:
                pass
        linear_distance_ints = []
        for i in range(len(linear_distance)):
            try:
                linear_distance_ints.append((linear_distance[i+1]-linear_distance[i]))
            except:
                pass
        time_ints = []
        for i in range(len(time)):
            try:
                time_ints.append((time[i+1]-time[i]))
            except:
                pass
        average_velocity = []
        for dis, tim in zip(linear_distance_ints, time_ints):
            try:
                average_velocity.append(abs(dis/tim))
            except:
                pass
        plot_time = []
        for i in range(len(time)):
            try:
                plot_time.append((time[i+1]+time[i])/2)
            except:
                pass

        plot_time = plot_time[:-1]

##        linear_distance_ints = [(linear_distance[i+1]-linear_distance[i]) for i in range(len(linear_distance)-1)]
##        time_ints = [(time[i+1]-time[i]) for i in range(len(time)-1)]
##        avg_velocity = [dis/tim for dis,tim in zip(linear_distance_ints, time_ints)]
##        plot_time = [(time[i+1]+time[i])/2 for i in range(len(time)-1)]
##        plot_time = deque(itertools.islice(time, 1, len(plot_time)))

        fig = plt.figure()
        fig.canvas.set_window_title("Trial %s Average Velocity" %(self.cmBox1.currentText()))
        plt.plot(plot_time, average_velocity, marker='.', linestyle='-')
        plt.xlabel("Time (s)")
        plt.ylabel("Average Velocity (cm/s)")
        plt.show()


# main =============================================
    
def main():
    app = Qt.QApplication(sys.argv)
    window = Window()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
