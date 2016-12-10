from PyQt4 import Qt
from nanpy import (SerialManager, ArduinoApi)
from collections import (OrderedDict, deque)
import graphical_programming_v5
import sys

class ArduinoWizard(Qt.QWizard):
    NUM_PAGES = 2

    (PagePinAssign, PageMethods) = range(NUM_PAGES)

    def __init__(self, arduino_sp, parent=None):
        super(ArduinoWizard, self).__init__(parent)

        global ard_setup_parameters
        ard_setup_parameters = arduino_sp

        self.setPage(self.PagePinAssign, PinAssignPage())
        self.setPage(self.PageMethods, MethodsPage())

        self.setStartId(self.PagePinAssign)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ClassicStyle)
        self.setOption(self.HaveHelpButton, True)

        self.setWindowTitle(self.tr("Arduino Setup Wizard"))

        self.setFixedSize(1250,750)

class PinAssignPage(Qt.QWizardPage):
                      
    def __init__(self, parent=None):
        super(PinAssignPage, self).__init__(parent)

        self.setTitle(self.tr("Arduino Pin Assignments"))

        self.board_pins = ["2 (D2)", "3 (D3)", "4 (D4)", "5 (D5)", "6 (D6)", "7 (D7)", "8 (D8)", "9 (D9)", "10 (D10)", "11 (D11)", "12 (D12)", "14 (A0)", "15 (A1)", "16 (A2)", "17 (A3)", "18 (A4)", "19 (A5)"]

        self.table = Qt.QTableWidget(self)
        self.table.setRowCount(17)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["pin #", "var_name", "INPUT/OUTPUT", "ANALOG/DIGITAL"])
        self.table.setVerticalHeaderLabels(self.board_pins)
        self.table.horizontalHeader().setResizeMode(Qt.QHeaderView.Stretch)
        self.table.verticalHeader().setResizeMode(Qt.QHeaderView.Stretch)

        global ard_setup_parameters
        
        for i, pin_num in enumerate(self.board_pins):
            self.table.setItem(i, 0, Qt.QTableWidgetItem(pin_num.split(' ')[0]))
            try:
                if pin_num.split(' ')[0] in ard_setup_parameters['pins'].keys():
                    self.table.setItem(i, 1, Qt.QTableWidgetItem(ard_setup_parameters['pins'][pin_num.split(' ')[0]][0]))
                else:
                   self.table.setItem(i, 1, Qt.QTableWidgetItem("-")) 
            except:
                self.table.setItem(i, 1, Qt.QTableWidgetItem("-"))
        for i, pin_num in enumerate(self.board_pins):
            cmBox1 = Qt.QComboBox()
            cmBox1.addItems(["INPUT", "OUTPUT"])
        
            cmBox2 = Qt.QComboBox()
            cmBox2.addItems(["ANALOG", "DIGITAL"])
                    
            if int(pin_num.split(' ')[0]) < 13:
                self.table.setCellWidget(i, 2, cmBox1)
                try:
                    if pin_num.split(' ')[0] in ard_setup_parameters['pins'].keys():
                        if ard_setup_parameters['pins'][pin_num.split(' ')[0]][1] == "OUTPUT":
                            self.table.cellWidget(i, 2).setCurrentIndex(1)
                except:
                    pass
                self.table.setItem(i, 3, Qt.QTableWidgetItem("DIGITAL"))
            elif int(pin_num.split(' ')[0]) > 13:
                self.table.setItem(i, 2, Qt.QTableWidgetItem("INPUT"))
                self.table.setCellWidget(i, 3, cmBox2)
                try:
                    if pin_num.split(' ')[0] in ard_setup_parameters['pins'].keys():
                        if ard_setup_parameters['pins'][pin_num.split(' ')[0]][2] == "DIGITAL":
                            self.table.cellWidget(i, 3).setCurrentIndex(1)
                except:
                    pass
    
        self.pshBtn1 = Qt.QPushButton(self.tr("ASSIGN PINS"))
        self.pshBtn1.clicked.connect(self.assign_pins)
        
        #self.registerField("Built?*", self.pshBtn1)    

        layout1 = Qt.QVBoxLayout()
        layout1.addWidget(self.table)
            
        layout2 = Qt.QHBoxLayout()
        layout2.addWidget(self.pshBtn1)
    
        layout1.addLayout(layout2)
    
        self.setLayout(layout1)

    def assign_pins(self):
        global pins
        pins = OrderedDict()
        for i, pin in enumerate(self.board_pins):
            try:
                if self.table.item(i, 1).text() != '-':
                    if int(pin.split(' ')[0]) < 13:
                        pins[self.table.item(i, 0).text()] = [self.table.item(i, 1).text(), self.table.cellWidget(i, 2).currentText(), self.table.item(i, 3).text()]
                    elif int(pin.split(' ')[0]) > 13:
                        pins[self.table.item(i, 0).text()] = [self.table.item(i, 1).text(), self.table.item(i, 2).text(), self.table.cellWidget(i, 3).currentText()]
            except:
                pass
        global ard_setup_parameters
        try:
            ard_setup_parameters["pins"] = pins
        except:
            ard_setup_parameters = {"pins":pins}

    def nextId(self):
        return ArduinoWizard.PageMethods

class MethodsPage(Qt.QWizardPage):
            
    def __init__(self, parent=None):
        super(MethodsPage, self).__init__(parent)

        self.setTitle(self.tr("Program the Arduino"))

        self.pshBtn1 = Qt.QPushButton(self.tr("LOAD PINS"))
        self.pshBtn1.clicked.connect(self.load_pins)

        self.pshBtn2 = Qt.QPushButton(self.tr("FINALISE CODE"))
        self.pshBtn2.clicked.connect(self.finalise_code)
        self.pshBtn2.setEnabled(False)

        layout1 = Qt.QHBoxLayout()
        layout1.addWidget(self.pshBtn1)
        layout1.addWidget(self.pshBtn2)
        layout1.addStretch(True)

        self.layout2 = Qt.QVBoxLayout()
        self.layout2.addLayout(layout1)

        self.setLayout(self.layout2)

    def nextId(self):
        return -1

    def load_pins(self):
        try:
            self.layout2.removeWidget(self.graph_prog_term)
            self.graph_prog_term.deleteLater()
            self.graph_prog_term = None
        except:
            pass
        global ard_setup_parameters
        pins = ard_setup_parameters["pins"]
        self.graph_prog_term = graphical_programming_v5.MainWindow(pins_assigned=pins, arduino_sp=ard_setup_parameters)
        self.layout2.addWidget(self.graph_prog_term)
        self.setLayout(self.layout2)
        self.adjustSize()
        self.pshBtn2.setEnabled(True)

    def finalise_code(self):
        global ard_setup_parameters
        from graphical_programming_v5 import instructions_list
        description = instructions_list['description']
        naming_list = instructions_list['naming_list']
        setup_list = instructions_list['setup_list']
        loop_list = instructions_list['loop_list']
        ard_setup_parameters["description"] = description
        ard_setup_parameters["naming_list"] = naming_list
        ard_setup_parameters["setup_list"] = setup_list
        ard_setup_parameters["loop_list"] = loop_list
        print("new DAAC setup: %s" %(ard_setup_parameters))
        
             
# main ==========================================

def main():
    app = Qt.QApplication(sys.argv)
    awiz = ArduinoWizard()
    awiz.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
