# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 19:55:31 2016

@author: Matt
"""
    
from PyQt4 import Qt
import csv
import sys

class Results(Qt.QDialog):
    def __init__(self, parent=None):
        super(Results, self).__init__(parent)
        
        global global_results
        from OneStopTrack import global_results
        
        self.setWindowTitle(self.tr("Raw Data"))        

        self.cmBox1 = Qt.QComboBox()
        for key in global_results.keys():
            self.cmBox1.addItem(str(key))

        label1 = Qt.QLabel("Date")
        self.lneEdt1 = Qt.QLineEdit()
  
        label2 = Qt.QLabel("Start Time")
        self.lneEdt2 = Qt.QLineEdit()

        label3 = Qt.QLabel("End Time")
        self.lneEdt3 = Qt.QLineEdit()

        label4 = Qt.QLabel("Duration (sec)")
        self.lneEdt4 = Qt.QLineEdit()

        label5 = Qt.QLabel("Comments")
        self.txtEdt1 = Qt.QTextEdit()

        self.cmBox2 = Qt.QComboBox()

        self.pshBtn1 = Qt.QPushButton("Show Trial")
        self.pshBtn1.clicked.connect(self.change_trial)
            
        self.pshBtn2 = Qt.QPushButton("Show Variable")
        self.pshBtn2.clicked.connect(self.change_var)
        
        self.pshBtn3 = Qt.QPushButton(self.tr('EXPORT TRIAL'))
        self.pshBtn3.clicked.connect(self.export_trial)
        
        self.table = Qt.QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(1)
        self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.resizeColumnsToContents()

        layout1 = Qt.QFormLayout()
        layout1.addRow(self.cmBox1)
        layout1.addRow(self.pshBtn1)
        layout1.addRow(label1, self.lneEdt1)
        layout1.addRow(label2, self.lneEdt2)
        layout1.addRow(label3, self.lneEdt3)
        layout1.addRow(label4, self.lneEdt4)
        layout1.addRow(label5, self.txtEdt1)
        
        layout2 = Qt.QVBoxLayout()
        layout2.addWidget(self.cmBox2)
        layout2.addWidget(self.pshBtn2)
        layout2.addWidget(self.table)

        layout3 = Qt.QHBoxLayout()
        layout3.addLayout(layout1)
        layout3.addLayout(layout2)

        layout4 = Qt.QVBoxLayout()
        layout4.addWidget(self.pshBtn3)
        layout4.insertStretch(1)

        layout5 = Qt.QHBoxLayout()
        layout5.addLayout(layout3)
        layout5.addLayout(layout4) 
                
        self.setLayout(layout5)
        
        #self.setGeometry(50, 50, 250, 600)

    def change_trial(self):
        try:
            self.lneEdt1.clear()
            self.lneEdt2.clear()
            self.lneEdt3.clear()
            self.lneEdt4.clear()
            self.txtEdt1.clear()
            self.cmBox2.clear()
            self.table.clear()
            for key in global_results[self.cmBox1.currentText()]["results"].keys():
                self.cmBox2.addItem(key)
            self.lneEdt1.setText(global_results[self.cmBox1.currentText()]["trial_info"]["Date"])
            self.lneEdt2.setText(global_results[self.cmBox1.currentText()]["trial_info"]["Start_Time"])
            self.lneEdt3.setText(global_results[self.cmBox1.currentText()]["trial_info"]["End_Time"])
            self.lneEdt4.setText(global_results[self.cmBox1.currentText()]["trial_info"]["Trial_Duration"])
            try:
                self.txtEdt1.setText(global_results[self.cmBox1.currentText()]["trial_info"]["Comments"])
            except:
                pass
        except:
            print("Error! Can't display current trial or can't change to other trials")
            
    def change_var(self):
        #try:
        self.table.clear()
        self.table.setRowCount(len(global_results[self.cmBox1.currentText()]["results"][str(self.cmBox2.currentText())]))
        for i, tem in enumerate(global_results[self.cmBox1.currentText()]["results"][self.cmBox2.currentText()]):
            if self.cmBox2.currentText() == 'position':
                try:
                    pos_x = round(tem[0],2)
                    pos_y = round(tem[1],2)
                except:
                    pos_x = round(eval(tem)[0],2)
                    pos_y = round(eval(tem)[1],2)
                self.table.setItem(i, 0, Qt.QTableWidgetItem(str((pos_x,pos_y))))
            else:
                self.table.setItem(i, 0, Qt.QTableWidgetItem(str(tem)))
        #except:
            #print("Error! Can't display current variable or can't change to other variables")

    def export_trial(self):
        name = Qt.QFileDialog.getSaveFileName(self, 'Export Trial Results') 
        with open(name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", self.lneEdt1.text()])
            writer.writerow(["Start_Time", self.lneEdt2.text()])
            writer.writerow(["End_Time", self.lneEdt3.text()])
            writer.writerow(["Trial_Duration", self.lneEdt4.text()])
            writer.writerow(["Comments", self.txtEdt1.toPlainText()])
            for key in global_results[self.cmBox1.currentText()]["results"].keys():
                temp_list = [key]
                for i in global_results[self.cmBox1.currentText()]["results"][key]:
                    temp_list.append(i)
                writer.writerow(temp_list)
        print("exported result: %s" %(name))

                
# main ===============================================               

def main():
    app = Qt.QApplication(sys.argv)
    results = Results()
    results.show()
    
    sys.exit(app.exec_())   

if __name__ == '__main__':
    main()
