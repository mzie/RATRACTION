# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 19:55:31 2016

@author: Matt
"""

#import sys
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
#
#class tabdemo(QTabWidget):
#   def __init__(self, parent = None):
#      super(tabdemo, self).__init__(parent)
#      self.tab1 = QWidget()
#      self.tab2 = QWidget()
#      self.tab3 = QWidget()
#		
#      self.addTab(self.tab1,"Tab 1")
#      self.addTab(self.tab2,"Tab 2")
#      self.addTab(self.tab3,"Tab 3")
#      self.tab1UI()
#      self.tab2UI()
#      self.tab3UI()
#      self.setWindowTitle("tab demo")
#		
#   def tab1UI(self):
#      layout = QFormLayout()
#      layout.addRow("Name",QLineEdit())
#      layout.addRow("Address",QLineEdit())
#      self.setTabText(0,"Contact Details")
#      self.tab1.setLayout(layout)
#		
#   def tab2UI(self):
#      layout = QFormLayout()
#      sex = QHBoxLayout()
#      sex.addWidget(QRadioButton("Male"))
#      sex.addWidget(QRadioButton("Female"))
#      layout.addRow(QLabel("Sex"),sex)
#      layout.addRow("Date of Birth",QLineEdit())
#      self.setTabText(1,"Personal Details")
#      self.tab2.setLayout(layout)
#		
#   def tab3UI(self):
#      layout = QHBoxLayout()
#      layout.addWidget(QLabel("subjects")) 
#      layout.addWidget(QCheckBox("Physics"))
#      layout.addWidget(QCheckBox("Maths"))
#      self.setTabText(2,"Education Details")
#      self.tab3.setLayout(layout)
#		
#def main():
#   app = QApplication(sys.argv)
#   ex = tabdemo()
#   ex.show()
#   sys.exit(app.exec_())
#	
#if __name__ == '__main__':
#   main()

#from PyQt4 import QtGui
#
#class Table(QtGui.QDialog):
#    def __init__(self, parent=None):
#        super(Table, self).__init__(parent)
#        layout = QtGui.QGridLayout() 
#        self.cmBox = QtGui.QComboBox()
#        self.cmBox.addItems(["Time", "Distance", "Velocity"])
#        self.cmBox.currentIndexChanged.connect(self.changed)
#        self.table = QtGui.QTableWidget()
#        #self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
#        self.table.setRowCount(10)
#        self.table.setColumnCount(5)
#        layout.addWidget(self.cmBox, 0, 0)
#        layout.addWidget(self.table, 1, 0)
#        self.table.setItem(1, 0, QtGui.QTableWidgetItem(self.cmBox.currentText()))
#        self.setLayout(layout)
#        
#    def changed(self):
#        print("hello")
#       
#
#def main():
#    import sys
#    app = 0
#    app = QtGui.QApplication(sys.argv)
#    t = Table()
#    t.show()
#    sys.exit(app.exec_())   
#
#if __name__ == '__main__':
#    main()
    
from PyQt4 import Qt
import csv

class Table(Qt.QDialog):
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        
        global results
        from OneStopTrack import results
        
        self.setWindowTitle(self.tr("Raw Data"))        
                
        self.cmBox = Qt.QComboBox()
        for key in results.keys():
            self.cmBox.addItem(key)
            
        self.pshBtn1 = Qt.QPushButton()
        self.pshBtn1.clicked.connect(self.change_var)
        
        self.pshBtn2 = Qt.QPushButton(self.tr('EXPORT'))
        self.pshBtn2.clicked.connect(self.export)
        
        self.pshBtn3 = Qt.QPushButton(self.tr('EXPORT ALL'))
        self.pshBtn3.clicked.connect(self.export_all)
        
        self.table = Qt.QTableWidget()
        
        self.maxLen = 0
        for key in results.keys():
            if len(results[key]) > self.maxLen:
                self.maxLen = len(results[key])
        for key in results.keys():
            while len(results[key]) < self.maxLen:
                results[key].extend(['null'])
        
        self.table.setRowCount(self.maxLen)
        self.table.setColumnCount(1)
        self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.resizeColumnsToContents()
        
        layout1 = Qt.QVBoxLayout()
        layout1.addWidget(self.cmBox)
        layout1.addWidget(self.pshBtn1)
        layout1.addWidget(self.table)

        layout2 = Qt.QVBoxLayout()
        layout2.insertStretch(0)
        layout2.addWidget(self.pshBtn2)
        layout2.addWidget(self.pshBtn3)

        layout3 = Qt.QHBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)  
                
        self.setLayout(layout3)
        
        self.setGeometry(50, 50, 250, 600)

    def change_var(self):
        self.table.clear()
        for i, tem in enumerate(results[self.cmBox.currentText()]):
            self.table.setItem(i, 0, Qt.QTableWidgetItem(str(tem)))

    def export(self):
        name = Qt.QFileDialog.getSaveFileName(self, 'Save File') 
        with open(name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.cmBox.currentText()])
            for val in results[self.cmBox.currentText()]:
                type(val)
                writer.writerow([str(val)])

    def export_all(self):
        name = Qt.QFileDialog.getSaveFileName(self, 'Save File') 
        with open(name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(results.keys())
            count = 0
            while count < self.maxLen:
                temprow = []
                for sublist in results.values():
                    temprow.append(sublist[count])
                writer.writerow(temprow)
                count += 1
                

def main():
    import sys
    app = 0
    app = Qt.QApplication(sys.argv)
    t = Table()
    t.show()
    sys.exit(app.exec_())   

if __name__ == '__main__':
    main()