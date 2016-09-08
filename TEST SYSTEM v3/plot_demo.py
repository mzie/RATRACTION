# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:58:14 2016

@author: Matt
"""

from PyQt4 import Qt
import matplotlib.pyplot as plt

class Plot(Qt.QWidget):
    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)
        
        
        global results
        from OneStopTrack import results
        
        self.button = Qt.QPushButton('Plot', self)
        self.button.clicked.connect(self.handleButton)
        self.cmBox1 = Qt.QComboBox()
        self.cmBox1.addItem("")
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItem("")
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItem("")
        for var in results.keys():
            self.cmBox1.addItem(var)
            self.cmBox2.addItem(var)
        layout = Qt.QVBoxLayout(self)
        layout.addWidget(self.cmBox1)
        layout.addWidget(self.cmBox2)
        layout.addWidget(self.button)

    def handleButton(self):
        plt.plot(results[self.cmBox1.currentText()],results[self.cmBox2.currentText()])
        plt.show()

def main():
    import sys
    app = Qt.QApplication(sys.argv)
    plot = Plot()
    plot.show()
    sys.exit(app.exec_())	

if __name__ == '__main__':
    main()