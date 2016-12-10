# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:54:18 2016

@author: Matt
"""
# import necessary packages and modules
from PyQt4 import Qt
from PyQt4 import (QtGui, QtCore)
import sys
import csv
from time import sleep
from collections import OrderedDict
import OneStopTrack
import raw_data_viewer
import grid_time_analysis
import roi_time_analysis
import animal_movement_scatterplot
import animal_movement_heatmap
import locomotor_parameters

class MyWindow(Qt.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.initUI()
        
        main_widget = OneStopTrack.Window()
             
        self.setCentralWidget(main_widget)

        #self.statusBar()
        #self.statusBar().setSizeGripEnabled(False)

        self.show()
        
        Qt.QApplication.setStyle(Qt.QStyleFactory.create('Windows')) 

        global global_results
        global_results = {}

    def initUI(self):               
        exitAction = Qt.QAction("&Quit", self)
        #exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        view_results = Qt.QAction("&View Raw Data", self)
        view_results.triggered.connect(self.view_results)  

        load_results = Qt.QAction("&Load Raw Data", self)
        load_results.triggered.connect(self.load_results)

        analyseResults1 = Qt.QAction("&Grid Time Analysis", self)
        analyseResults1.triggered.connect(self.grid_time_analysis)

        analyseResults2 = Qt.QAction("ROI Time Analysis", self)
        analyseResults2.triggered.connect(self.roi_time_analysis)

        analyseResults3 = Qt.QAction("&Animal Movement Scatterplot", self)
        analyseResults3.triggered.connect(self.animal_movement_scatterplot)

        analyseResults4 = Qt.QAction("&Animal Movement Heatmap", self)
        analyseResults4.triggered.connect(self.animal_movement_heatmap)

        analyseResults5 = Qt.QAction("&Locomotor Parameters", self)
        analyseResults5.triggered.connect(self.locomotor_parameters)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        resultsMenu = menubar.addMenu("&Results")
        resultsMenu.addAction(view_results)
        resultsMenu.addSeparator()
        resultsMenu.addAction(load_results)
        
        analysisMenu = menubar.addMenu("&Data Analysis")
        analysisMenu.addAction(analyseResults1)
        analysisMenu.addAction(analyseResults2)
        analysisMenu.addAction(analyseResults3)
        analysisMenu.addAction(analyseResults4)
        analysisMenu.addAction(analyseResults5)
                
        self.setMinimumWidth(1150)
        #self.setMinimumHeight(800)
        self.setWindowTitle(self.tr("RATRACTION"))
        self.show()
               
    def view_results(self): 
        self.results = raw_data_viewer.Results()
        self.results.show()

    def load_results(self):
        try:
            temp_dict = {"trial_info":{},"results":{}}
            name = Qt.QFileDialog.getOpenFileName(self, 'Load Results File')
            with open(name, 'r') as f:
                reader = csv.reader(f)
                for row in enumerate(reader):
                    if row[0] < 5:
                        temp_dict["trial_info"].update({row[1][0]:row[1][1]})
                    else:
                        temp_dict["results"].update({row[1][0]:row[1][1:]})
            OneStopTrack.global_results.update({name:temp_dict})
            print("loaded result: %s" %(name))
            return OneStopTrack.global_results
        except:
            pass
        
    def animal_movement_scatterplot(self):
        self.scatterplot = animal_movement_scatterplot.Scatter()
        self.scatterplot.show()

    def animal_movement_heatmap(self):
        self.heatmap = animal_movement_heatmap.Window()
        self.heatmap.show()

    def grid_time_analysis(self):
        self.grid_time = grid_time_analysis.Window()
        self.grid_time.show()

    def roi_time_analysis(self):
        self.roi_time = roi_time_analysis.Window()
        self.roi_time.show()

    def locomotor_parameters(self):
        self.parameters = locomotor_parameters.Window()
        self.parameters.show()


# main ===============================================

def main():
    app = Qt.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    
    sys.exit(app.exec_())   

if __name__ == '__main__':
    main()  
