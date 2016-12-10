# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 00:53:41 2016

@author: Matt
"""

from PyQt4 import Qt
from collections import OrderedDict
import sys

class MainWindow(Qt.QMainWindow):

    def __init__(self, pins_assigned, arduino_sp, parent=None):
        '''
        Constructor
        '''
        Qt.QMainWindow.__init__(self, parent)
        self.central_widget = Qt.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.start_screen = Start(pins_assigned)
        self.second_screen = Second(arduino_sp)
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.second_screen)
        self.central_widget.setCurrentWidget(self.start_screen)

        self.start_screen.click.connect(lambda: self.central_widget.setCurrentWidget(self.second_screen))
        self.second_screen.click.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))

        global ainputs, dinputs, outputs, other

        ainputs = []
        dinputs = []
        outputs = []

        for key in pins_assigned.keys():
            if pins_assigned[key][1] == "INPUT":
                if pins_assigned[key][2] == "ANALOG":
                    ainputs.append(pins_assigned[key][0])
                elif pins_assigned[key][2] == "DIGITAL":
                    dinputs.append(pins_assigned[key][0])
            elif pins_assigned[key][1] == "OUTPUT":
                outputs.append(pins_assigned[key][0])
        other = ["vidTrack_time", "ard_loop_time", "pos", "self.actButton1_on", "self.actButton2_on", "self.actButton3_on",
                 "self.actButton4_on","self.actButton5_on", "self.actButton6_on", "self.actButton7_on", "self.actButton8_on"]
                      
class Start(Qt.QWidget):

    click = Qt.pyqtSignal()
    
    def __init__(self, pins_assigned, parent=None):
        super(Start, self).__init__(parent)

        self.pins = pins_assigned

        self.tabs2 = Qt.QTabWidget()

        self.tab_2_1 = Qt.QWidget()
        self.tab_2_2 = Qt.QWidget()
        self.tab_2_3 = Qt.QWidget()
        self.tab_2_4 = Qt.QWidget()

        self.tabs2.addTab(self.tab_2_4, "Description")
        self.tabs2.addTab(self.tab_2_1, "Naming")
        self.tabs2.addTab(self.tab_2_2, "Setup")
        self.tabs2.addTab(self.tab_2_3, "Looping")
        self.tab_2_1UI()
        self.tab_2_2UI()
        self.tab_2_3UI()
        self.tab_2_4UI()
        self.tabs2.setCurrentIndex(3)

        self.run = Qt.QPushButton('Run')
        self.run.clicked.connect(self.runcode)   
       
        self.tp = Qt.QPushButton("To Text Programming")
        self.tp.clicked.connect(self._build)
        self.tp.clicked.connect(self.click.emit)
        
        self.upBtn = Qt.QPushButton()
        self.upBtn.setIcon(Qt.QIcon("up_icon.png"))
        self.upBtn.clicked.connect(self.moveCurrentRowUp)
        
        self.dwnBtn = Qt.QPushButton()
        self.dwnBtn.setIcon(Qt.QIcon("down_icon.png"))
        self.dwnBtn.clicked.connect(self.moveCurrentRowDown)
        
        self.delBtn = Qt.QPushButton()
        self.delBtn.setIcon(Qt.QIcon("close_x.png"))
        self.delBtn.clicked.connect(self.delCurrentRow)

        self.tabs = Qt.QTabWidget()
        
        self.tab1 = Qt.QWidget()
        self.tab2 = Qt.QWidget()
        self.tab3 = Qt.QWidget()
        self.tab4 = Qt.QWidget()

        self.tabs.addTab(self.tab1, "Tasks")
        self.tabs.addTab(self.tab2, "Decisions")
        self.tabs.addTab(self.tab3, "Repetition")
        self.tabs.addTab(self.tab4, "Subprograms")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

#        policy = self.tabs.sizePolicy()
#        policy.setHorizontalStretch()
#        self.tabs.setSizePolicy(policy)

        self.tabs.setFixedWidth(300)

        self.layout1 = Qt.QHBoxLayout()
        self.layout1.addWidget(self.tp)  
        self.layout1.addWidget(self.run)
        self.layout1.addStretch()

        self.layout2 = Qt.QHBoxLayout()  
        self.layout2.addWidget(self.upBtn)
        self.layout2.addWidget(self.dwnBtn)
        self.layout2.addWidget(self.delBtn)
        self.layout2.addStretch()

        self.layout3 = Qt.QVBoxLayout()
        self.layout3.addLayout(self.layout1)
        self.layout3.addLayout(self.layout2)
        self.layout3.addWidget(self.tabs2)       

        self.layout4 = Qt.QHBoxLayout()
        self.layout4.addWidget(self.tabs)
        self.layout4.addLayout(self.layout3)

        self.setLayout(self.layout4)

        self.connect(self.tabs2, Qt.SIGNAL('currentChanged(int)'), self.selector)

        self.setMinimumSize(1200,600)

    def selector(self, selected_index):
        if selected_index == 0:
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.upBtn.setEnabled(False)
            self.dwnBtn.setEnabled(False)
            self.delBtn.setEnabled(False)
            
        elif selected_index == 1:
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.upBtn.setEnabled(False)
            self.dwnBtn.setEnabled(False)
            self.delBtn.setEnabled(False)

        elif selected_index == 2:
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
            self.tabs.setTabEnabled(3, False)
            self.upBtn.setEnabled(False)
            self.dwnBtn.setEnabled(False)
            self.delBtn.setEnabled(False)

        elif selected_index == 3:
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(2, True)
            self.tabs.setTabEnabled(3, True)
            self.upBtn.setEnabled(True)
            self.dwnBtn.setEnabled(True)
            self.delBtn.setEnabled(True)

    def _build(self):
        global instructions_list
        instructions_list = {}
        naming_list = []
        setup_list = []
        loop_list = []
        naming_items = (self.table1.cellWidget(i, 0) for i in list(range(self.table1.rowCount())))
        for item in naming_items:
            naming_list.append(item.text())
        setup_items = (self.table2.cellWidget(i, 0) for i in list(range(self.table2.rowCount())))
        for item in setup_items:
            setup_list.append(item.text())
        list_items = (self.table.cellWidget(i, 0) for i in list(range(self.table.rowCount())))
        for item in list_items:
            loop_list.append(item.get_instructions())
        description = self.txtEdt1.toPlainText()
        instructions_list = {'description':description,'naming_list':naming_list, 'setup_list':setup_list, 'loop_list':loop_list}
        
    def runcode(self):
        self._build()

    def moveCurrentRowUp(self):
        row = self.table.currentRow()
        if row > 0:
            self.table.insertRow(row-1)
            self.table.setCellWidget(row-1,0,self.table.cellWidget(row+1,0))
            self.table.setCurrentCell(row-1,0)
            self.table.removeRow(row+1)  
    
    def moveCurrentRowDown(self):
        row = self.table.currentRow()
        if row < self.table.rowCount()-1:
            self.table.insertRow(row+2)
            self.table.setCellWidget(row+2,0,self.table.cellWidget(row,0))
            self.table.setCurrentCell(row+2,0)
            self.table.removeRow(row) 
           
    def delCurrentRow(self):
        row = self.table.currentRow()
        self.table.removeRow(row)
        self.table_row_count -= 1
    
    def update_table_rows(self):
        self.table_row_count += 1
        self.table.setRowCount(self.table_row_count)
        
    def tab1UI(self):
        
        self.addButton1 = Qt.QPushButton("Analog Read")
        self.addButton1.clicked.connect(self.addWidget1)
 
        self.addButton2 = Qt.QPushButton("Digital Read")
        self.addButton2.clicked.connect(self.addWidget2)

        self.addButton3 = Qt.QPushButton("Digital Write")
        self.addButton3.clicked.connect(self.addWidget3)
        
        self.addButton4 = Qt.QPushButton("Sleep")
        self.addButton4.clicked.connect(self.addWidget4)
       
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.addButton1)
        layout.addWidget(self.addButton2)
        layout.addWidget(self.addButton3)
        layout.addWidget(self.addButton4)
        layout.addStretch(True)
        self.tab1.setLayout(layout)

    def tab2UI(self):
        
        self.addButton5 = Qt.QPushButton("do Y if X something W else do Z")
        self.addButton5.clicked.connect(self.addWidget5)

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.addButton5)
        layout.addStretch(True)
        self.tab2.setLayout(layout)

    def tab3UI(self):
        
        self.addButton6 = Qt.QPushButton("for i in X do Y")
        self.addButton6.clicked.connect(self.addWidget6)

        self.addButton7 = Qt.QPushButton("while X do Y")
        self.addButton7.clicked.connect(self.addWidget7)
        
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.addButton6)
        layout.addWidget(self.addButton7)
        layout.addStretch(True)
        self.tab3.setLayout(layout)

    def tab4UI(self):

        pass        

    def addWidget1(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton1())
      
    def addWidget2(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton2())

    def addWidget3(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton3())

    def addWidget4(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton4())

    def addWidget5(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton5())

    def addWidget6(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton6())

    def addWidget7(self):
        self.update_table_rows()
        self.table.setCellWidget(self.table_row_count-1, 0, TestButton7())

    def tab_2_1UI(self):
          
        self.table1 = Qt.QTableWidget(self)
        self.table1_row_count = 0
        self.table1.setRowCount(self.table1_row_count)
        self.table1.setColumnCount(1)
        #self.table1.setShowGrid(False)
        self.table1.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table1.horizontalHeader().setVisible(False)
        self.table1.verticalHeader().setDefaultSectionSize(40)
        self.table1.setSelectionBehavior(Qt.QTableWidget.SelectRows)
        self.table1.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
        
        self.table1_row_count = len(self.pins)
        self.table1.setRowCount(self.table1_row_count)
        for i, key in enumerate(self.pins.keys()):
            temp_label = Qt.QLabel("%s = %s" %(self.pins[key][0], key))
            temp_label.setIndent(10)
            self.table1.setCellWidget(i, 0, temp_label)

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.table1)
        
        self.tab_2_1.setLayout(layout)

    def tab_2_2UI(self):
           
        self.table2 = Qt.QTableWidget(self)
        self.table2_row_count = 0
        self.table2.setRowCount(self.table2_row_count)
        self.table2.setColumnCount(1)
        #self.table2.setShowGrid(False)
        self.table2.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table2.horizontalHeader().setVisible(False)
        self.table2.verticalHeader().setDefaultSectionSize(40)
        self.table2.setSelectionBehavior(Qt.QTableWidget.SelectRows)
        self.table2.setSelectionMode(Qt.QAbstractItemView.SingleSelection)

        self.table2_row_count = len(self.pins)
        self.table2.setRowCount(self.table2_row_count)

        for i, key in enumerate(self.pins.keys()):
            if self.pins[key][1] == 'INPUT':
                temp_label = Qt.QLabel('a.pinMode(%s, a.INPUT)' % (self.pins[key][0]))
            elif self.pins[key][1] == 'OUTPUT':
                temp_label = Qt.QLabel('a.pinMode(%s, a.OUTPUT)' % (self.pins[key][0]))
            temp_label.setIndent(10)
            self.table2.setCellWidget(i, 0, temp_label)
       
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.table2)
        
        self.tab_2_2.setLayout(layout)       
        
    def tab_2_3UI(self):
           
        self.table = Qt.QTableWidget(self)
        self.table_row_count = 0
        self.table.setRowCount(self.table_row_count)
        self.table.setColumnCount(1)
        #self.table.setShowGrid(False)
        self.table.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setSelectionBehavior(Qt.QTableWidget.SelectRows)
        self.table.setSelectionMode(Qt.QAbstractItemView.SingleSelection)

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.table)
        
        self.tab_2_3.setLayout(layout)            

    def tab_2_4UI(self):

        self.txtEdt1 = Qt.QTextEdit()
        self.txtEdt1.setText("Replace this text with a description of what the Arduino method should do")  

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.txtEdt1)

        self.tab_2_4.setLayout(layout)
        
class Second(Qt.QWidget):

    click = Qt.pyqtSignal()

    def __init__(self, arduino_sp, parent=None):
        super(Second, self).__init__(parent)

        self.ard_setup_parameters = arduino_sp 

        self.gp = Qt.QPushButton("To Graphical Programming")
        self.gp.clicked.connect(self.click.emit)
    
        self.run = Qt.QPushButton('Run')
        self.run.clicked.connect(self.runcode)  
        
        self.build = Qt.QPushButton('Build')
        self.build.clicked.connect(self._build)

        self.tabs = Qt.QTabWidget()
        self.tab1 = Qt.QWidget()
        self.tab2 = Qt.QWidget()
        self.tab3 = Qt.QWidget()
        self.tab4 = Qt.QWidget()

        self.tabs.addTab(self.tab4, "Description")
        self.tabs.addTab(self.tab1, "Naming")
        self.tabs.addTab(self.tab2, "Setup")
        self.tabs.addTab(self.tab3, "Looping")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tabs.setCurrentIndex(3)

        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.gp)
        layout1.addWidget(self.build)
        layout1.addWidget(self.run)
        layout1.addStretch(True)

        layout2 = Qt.QHBoxLayout()
        layout2.addWidget(self.tabs) 
        
        layout2 = Qt.QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.tabs)
        
        self.setLayout(layout2)

        self.setMinimumSize(1200,600)

    def tab1UI(self):
 
        self.txtEdt = Qt.QTextEdit()
        try:
            for name in self.ard_setup_parameters['naming_list']:
                self.txtEdt.append(name)
        except:
            pass
        
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.txtEdt)
        
        self.tab1.setLayout(layout)     
 
    def tab2UI(self):
 
        self.txtEdt1 = Qt.QTextEdit()
        try:
            for line in self.ard_setup_parameters['setup_list']:
                self.txtEdt1.append(line)
        except:
            pass
        
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.txtEdt1)
        
        self.tab2.setLayout(layout)              

    def tab3UI(self): 

        self.txtEdt2 = Qt.QTextEdit()
        try:
            for line in self.ard_setup_parameters['loop_list']:
                self.txtEdt2.append(line)
        except:
            pass
        
        layout = Qt.QVBoxLayout()
        layout.addWidget(self.txtEdt2)
        
        self.tab3.setLayout(layout)       

    def tab4UI(self):

        self.txtEdt3 = Qt.QTextEdit()
        try:
            self.txtEdt3.setText(self.ard_setup_parameters['description'])
        except:
            pass

        layout = Qt.QVBoxLayout()
        layout.addWidget(self.txtEdt3)

        self.tab4.setLayout(layout)
                        
    def _build(self):
        self.txtEdt.clear()
        self.txtEdt1.clear()
        self.txtEdt2.clear()
        self.txtEdt3.clear()
        global instructions_list
        for name in instructions_list['naming_list']:
            self.txtEdt.append(name)
        for line in instructions_list['setup_list']:
           self.txtEdt1.append(line)
        for line in instructions_list['loop_list']:
            self.txtEdt2.append(line)
        self.txtEdt3.setText(instructions_list['description'])
    
    def runcode(self):
        global instructions_list
        instructions_list = {}
        naming_list = []
        setup_list = []
        loop_list = []
        for name in self.txtEdt.toPlainText().split('\n'):
            naming_list.append(name)
        for line in self.txtEdt1.toPlainText().split('\n'):
            setup_list.append(line)
        for line in self.txtEdt2.toPlainText().split('\n'):
            loop_list.append(line)
        description = self.txtEdt3.toPlainText()
        instructions_list = {'description':description, 'naming_list':naming_list, 'setup_list':setup_list, 'loop_list':loop_list}
            
class TestButton1(Qt.QWidget):
    '''
    analogRead(analog_input_pin)
    '''
    def __init__(self, parent=None):
        super(TestButton1, self).__init__(parent)
           
        self.label = Qt.QLabel("Analog Read")
        self.cmBox = Qt.QComboBox()
        self.cmBox.addItems(ainputs)
                
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.cmBox)
        layout.addStretch(True)
        self.setLayout(layout)
        
    def get_instructions(self): 
        instructions = 'ard_results["%s"].append(a.analogRead(%s))' %(self.cmBox.currentText(), self.cmBox.currentText())
        return instructions

class TestButton2(Qt.QWidget):  
    '''
    digitalRead(digital_input_pin)
    '''
    def __init__(self, parent=None):
        super(TestButton2, self).__init__(parent)
 
        self.label = Qt.QLabel("Digital Read")
        self.cmBox = Qt.QComboBox()
        self.cmBox.addItems(dinputs)
        
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.cmBox)
        layout.addStretch(True)
        self.setLayout(layout)

    def get_instructions(self): 
        instructions = 'ard_results["%s"].append(a.digitalRead(%s))' %(self.cmBox.currentText(), self.cmBox.currentText())
        return instructions

class TestButton3(Qt.QWidget):
    '''
    digitalWrite(output_pin, HIGH/LOW)
    '''
    def __init__(self, parent=None):
        super(TestButton3, self).__init__(parent)

        self.label = Qt.QLabel("Digital Write")   
        self.cmBox1 = Qt.QComboBox()
        self.cmBox1.addItems(outputs)
        self.cmBox2 = Qt.QComboBox() 
        self.cmBox2.addItems(["HIGH", "LOW"])
        
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.cmBox1)
        layout.addWidget(self.cmBox2)
        layout.addStretch(True)
        self.setLayout(layout)

    def get_instructions(self):
        instructions = 'a.digitalWrite(%s,a.%s)\nard_results["%s"].append("%s")' %(self.cmBox1.currentText(),self.cmBox2.currentText(),self.cmBox1.currentText(),self.cmBox2.currentText())
        return instructions
    
class TestButton4(Qt.QWidget):
    '''
    sleep(#_of_seconds)
    '''
    def __init__(self, parent=None):
        super(TestButton4, self).__init__(parent)

        self.label = Qt.QLabel("Sleep")
        self.spnBox = Qt.QSpinBox()        
        
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spnBox)
        layout.addStretch(True)
        self.setLayout(layout)

    def get_instructions(self): 
        instructions = 'sleep(%s)' %(str(self.spnBox.value()))
        return instructions

class TestButton5(Qt.QWidget):
    '''
    do Y if X something W else do Z
    '''
    def __init__(self, parent=None):
        super(TestButton5, self).__init__(parent)       
                
        self.label1 = Qt.QLabel("do")
        self.cmBox1 = Qt.QComboBox()
        self.cmBox1.addItems([("a.analogRead(%s)" %(item)) for item in ainputs])
        self.cmBox1.addItems([("a.digitalRead(%s)" %(item)) for item in dinputs])
        self.cmBox1.addItems([("a.digitalWrite(%s, a.HIGH)" %(item)) for item in outputs])
        self.cmBox1.addItems([("a.digitalWrite(%s, a.LOW)" %(item)) for item in outputs])
        self.label2 = Qt.QLabel("if")
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItems([("%s" %(item)) for item in outputs])
        self.cmBox2.addItems([("%s" %(item)) for item in ainputs])
        self.cmBox2.addItems([("%s" %(item)) for item in dinputs])
        self.cmBox2.addItems(other)
        self.cmBox3 = Qt.QComboBox()
        self.cmBox3.addItems([">", "<", "==", "!=", "in", "not in"])
        self.cmBox3.setCurrentIndex(3)
        self.lneEdt2 = Qt.QLineEdit()
        self.cmBox4 = Qt.QComboBox()
        self.cmBox4.setLineEdit(self.lneEdt2)
        self.cmBox4.addItems(["True", "False", "1", "0", "HIGH", "LOW", "None", "(TL_x,TL_y,BR_x,BR_y)"])
        self.label3 = Qt.QLabel("else do")
        self.cmBox5 = Qt.QComboBox()
        self.cmBox5.addItem("None")
        self.cmBox5.addItems([("a.analogRead(%s)" %(item)) for item in ainputs])
        self.cmBox5.addItems([("a.digitalRead(%s)" %(item)) for item in dinputs])
        self.cmBox5.addItems([("a.digitalWrite(%s, a.HIGH)" %(item)) for item in outputs])
        self.cmBox5.addItems([("a.digitalWrite(%s, a.LOW)" %(item)) for item in outputs])
                
        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.cmBox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.cmBox2)
        layout.addWidget(self.cmBox3)
        layout.addWidget(self.cmBox4)
        layout.addWidget(self.label3)
        layout.addWidget(self.cmBox5)
        layout.addStretch(True)
        self.setLayout(layout)

    def get_instructions(self):
        if (self.cmBox2.currentText() == "pos") and (self.cmBox3.currentText() == "in"):
            instructions = '%s if ((vid_tracking_methods.mod_pt[0] >= eval(str(%s))[0]) and (vid_tracking_methods.mod_pt[1] >= eval(str(%s))[1]) and (vid_tracking_methods.mod_pt[0] <= eval(str(%s))[2]) and (vid_tracking_methods.mod_pt[1] <= eval(str(%s))[3])) else %s' %(self.cmBox1.currentText(), self.lneEdt2.text(), self.lneEdt2.text(), self.lneEdt2.text(), self.lneEdt2.text(), self.cmBox5.currentText())
        elif (self.cmBox2.currentText() == "pos") and (self.cmBox3.currentText() == "not in"):
            instructions = '%s if (((vid_tracking_methods.mod_pt[0] <= eval(str(%s))[0]) or (vid_tracking_methods.mod_pt[0] >= eval(str(%s))[2])) or ((vid_tracking_methods.mod_pt[1] <= eval(str(%s))[1]) or (vid_tracking_methods.mod_pt[1] >= eval(str(%s))[3]))) else %s' %(self.cmBox1.currentText(), self.lneEdt2.text(), self.lneEdt2.text(), self.lneEdt2.text(), self.lneEdt2.text(), self.cmBox5.currentText())
        elif self.cmBox2.currentText() == "vidTrack_time":
            instructions = '%s if vid_tracking_methods.run_tme_ %s int(%s) else %s' %(self.cmBox1.currentText(), self.cmBox3.currentText(), self.lneEdt2.text(), self.cmBox5.currentText())
        elif self.cmBox2.currentText() == "ard_loop_time":
            instructions = '%s if current_loop_time %s int(%s) else %s' %(self.cmBox1.currentText(), self.cmBox3.currentText(), self.lneEdt2.text(), self.cmBox5.currentText())
        elif self.cmBox2.currentText() in outputs:
            instructions = '%s if ard_results["%s"][-1] %s "%s" else %s' %(self.cmBox1.currentText(), self.cmBox2.currentText(), self.cmBox3.currentText(), self.lneEdt2.text(), self.cmBox5.currentText())
        else:
            instructions = '%s if %s %s %s else %s' %(self.cmBox1.currentText(), self.cmBox2.currentText(), self.cmBox3.currentText(), self.lneEdt2.text(), self.cmBox5.currentText())
        return instructions 

class TestButton6(Qt.QWidget):
    '''
    for i in X do Y
    '''
    def __init__(self, parent = None):
        super(TestButton6, self).__init__(parent)     

        self.label1 = Qt.QLabel("for")

        self.lneEdt1 = Qt.QLineEdit()
        self.cmBox1 = Qt.QComboBox()
        self.cmBox1.setLineEdit(self.lneEdt1)

        self.label2 = Qt.QLabel("in")

        self.lneEdt2 = Qt.QLineEdit()
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.setLineEdit(self.lneEdt2)

        self.label3 = Qt.QLabel("do")

        self.lneEdt3 = Qt.QLineEdit()
        self.cmBox3 = Qt.QComboBox()
        self.cmBox3.setLineEdit(self.lneEdt3)

        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.cmBox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.cmBox2)
        layout.addWidget(self.label3)
        layout.addWidget(self.cmBox3)
        layout.addStretch(True)
        self.setLayout(layout)  

    def get_instructions(self):
        instructions = 'for %s in %s: %s' %(self.lneEdt1.text(),self.lneEdt2.text(),self.lneEdt3.text())
        return instructions
   
class TestButton7(Qt.QWidget):
    '''
    while X do Y
    '''
    def __init__(self, parent = None):
        super(TestButton7, self).__init__(parent) 
          
        self.label1 = Qt.QLabel("while")

        self.lneEdt1 = Qt.QLineEdit()
        self.cmBox1 = Qt.QComboBox()
        self.cmBox1.addItems([("a.digitalWrite(%s, a.HIGH)" %(item)) for item in outputs])
        self.cmBox1.addItems([("a.digitalWrite(%s, a.LOW)" %(item)) for item in outputs])
        self.cmBox1.addItems(other)
        self.cmBox1.setLineEdit(self.lneEdt1)

        self.label2 = Qt.QLabel("do")
        
        self.lneEdt2 = Qt.QLineEdit()
        self.cmBox2 = Qt.QComboBox()
        self.cmBox2.addItems([("a.analogRead(%s)" %(item)) for item in ainputs])
        self.cmBox2.addItems([("a.digitalRead(%s)" %(item)) for item in dinputs])
        self.cmBox2.addItems([("a.digitalWrite(%s, a.HIGH)" %(item)) for item in outputs])
        self.cmBox2.addItems([("a.digitalWrite(%s, a.LOW)" %(item)) for item in outputs])
        self.cmBox2.setLineEdit(self.lneEdt2)

        layout = Qt.QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.cmBox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.cmBox2)
        layout.addStretch(True)
        self.setLayout(layout)

    def get_instructions(self):
        instructions = 'while %s: %s' %(self.lneEdt1.text(), self.lneEdt2.text())
        return instructions


# main ==============================================

def main():
    app = Qt.QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
