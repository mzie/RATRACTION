from PyQt4 import Qt
#from nanpy import (SerialManager, ArduinoApi)
from collections import (OrderedDict, deque)

class ArduinoWizard(Qt.QWizard):
    NUM_PAGES = 3

    (PageConnect, PagePinAssign, PageMethods) = range(NUM_PAGES)

    def __init__(self, parent=None):
        super(ArduinoWizard, self).__init__(parent)

        self.setPage(self.PageConnect, ConnectPage(self))
        self.setPage(self.PagePinAssign, PinAssignPage())
        self.setPage(self.PageMethods, MethodsPage())

        self.setStartId(self.PageConnect)

        # images won't show in Windows 7 if style not set
        self.setWizardStyle(self.ModernStyle)
        self.setOption(self.HaveHelpButton, True)
        #self.setPixmap(Qt.QWizard.LogoPixmap, Qt.QPixmap("ironman.png"))

        self.setWindowTitle(self.tr("Arduino Wizard"))

class ConnectPage(Qt.QWizardPage):
    def __init__(self, parent=None):
        super(ConnectPage, self).__init__(parent)

        self.setTitle(self.tr("Establish Connection to Arduino"))
        #self.setPixmap(Qt.QWizard.WatermarkPixmap, Qt.QPixmap("ardlogo.png"))
        topLabel = Qt.QLabel(self.tr("Attempt to establish a connection to your Arduino microcontroller"))
        topLabel.setWordWrap(True)

        self.regRBtn = Qt.QRadioButton(self.tr("&Attempt to establish a connection to your Arduino microcontroller"))
        self.regRBtn.setChecked(False)
        self.regRBtn.clicked.connect(self.connect_to_arduino)

        self.registerField("Arduino Connected?*", self.regRBtn)

        layout = Qt.QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(self.regRBtn)
        self.setLayout(layout)

    def nextId(self):
        return ArduinoWizard.PagePinAssign

    def connect_to_arduino(self):
        try:
                global a
                connection = SerialManager()
                a = ArduinoApi(connection=connection)
        except:
                print("Failed to connect to Arduino")
                self.regRBtn.setChecked(True)               # change back to False

class PinAssignPage(Qt.QWizardPage):
    def build_pins(self):
        global pins
        pins = OrderedDict()
        for pio in self.LineEdits:
                try:
                    pins[pio.text().rsplit(' ', 4)[0]] = [pio.text().rsplit(' ', 4)[1], pio.text().rsplit(' ', 4)[2], pio.text().rsplit(' ', 4)[-1]]
                except:
                    pass
        print(pins.keys())
        print(pins)  
   
    def export_pins(self):
        name = Qt.QFileDialog.getSaveFileName(self, 'Save File')        
        with open(name, "w") as text_file:
                text_file.write(str(pins))
    
    def load_pins(self):
        name = Qt.QFileDialog.getOpenFileName(self, 'Open File')       
        with open(name, 'r') as f:        
               s = eval(f.read())
               #for (key, LineEdit, i) in zip(s.keys(), lineEdits, pinsnums):
               for key in s.keys():
                   for LineEdit, i in zip(self.LineEdits, self.pinsnums): 
                       if int(key) == i:
                           (LineEdit.setText(str(key) + ' ' + ' '.join(s[key][:])))

    def clear_pins(self):
        for LineEdit in self.LineEdits:
                LineEdit.clear()
    
    def __init__(self, parent=None):
        super(PinAssignPage, self).__init__(parent)

        self.setTitle(self.tr("Arduino Pin Assignments"))
        #self.setSubTitle(self.tr(""))

        boldFont = Qt.QFont()
        boldFont.setBold(True)
    
        dpinsLabel1 = Qt.QLabel("D Pins")
        dpinsLabel1.setFont(boldFont)
    
        dpinsLabel2 = Qt.QLabel("pin_#   var_name   INPUT/OUTPUT   DIGITAL")
        dpinsLabel2.setFont(boldFont)

        pin2Label = Qt.QLabel("2 (D2)")
        self.pin2LineEdit = Qt.QLineEdit()
        pin2Label.setBuddy(self.pin2LineEdit)
    
        pin3Label = Qt.QLabel("3 (D3)")
        self.pin3LineEdit = Qt.QLineEdit()
        pin3Label.setBuddy(self.pin3LineEdit)
 
        pin4Label = Qt.QLabel("4 (D4)")
        self.pin4LineEdit = Qt.QLineEdit()
        pin4Label.setBuddy(self.pin4LineEdit)

        pin5Label = Qt.QLabel("5 (D5)")
        self.pin5LineEdit = Qt.QLineEdit()
        pin5Label.setBuddy(self.pin5LineEdit)
   
        pin6Label = Qt.QLabel("6 (D6)")
        self.pin6LineEdit = Qt.QLineEdit()
        pin6Label.setBuddy(self.pin6LineEdit)

        pin7Label = Qt.QLabel("7 (D7)")
        self.pin7LineEdit = Qt.QLineEdit()
        pin7Label.setBuddy(self.pin7LineEdit)

        pin8Label = Qt.QLabel("8 (D8)")
        self.pin8LineEdit = Qt.QLineEdit() 
        pin8Label.setBuddy(self.pin8LineEdit)

        pin9Label = Qt.QLabel("9 (D9)")
        self.pin9LineEdit = Qt.QLineEdit()
        pin9Label.setBuddy(self.pin9LineEdit)

        pin10Label = Qt.QLabel("10 (D10)")
        self.pin10LineEdit = Qt.QLineEdit()
        pin10Label.setBuddy(self.pin10LineEdit)

        pin11Label = Qt.QLabel("11 (D11)")
        self.pin11LineEdit = Qt.QLineEdit()
        pin11Label.setBuddy(self.pin11LineEdit)

        pin12Label = Qt.QLabel("12 (D12)")
        self.pin12LineEdit = Qt.QLineEdit()
        pin12Label.setBuddy(self.pin12LineEdit)
    
        #pin13Label = Qt.QLabel("13 (D13)")
        #pin13LineEdit = Qt.QLineEdit()
        #pin13Label.setBuddy(pin13LineEdit)       
    
        apinsLabel1 = Qt.QLabel("A Pins")
        apinsLabel1.setFont(boldFont)
    
        apinsLabel2 = Qt.QLabel("pin_#   var_name   INPUT   ANALOG/DIGITAL")
        apinsLabel2.setFont(boldFont)        
    
        pin14Label = Qt.QLabel("14 (A0)")
        self.pin14LineEdit = Qt.QLineEdit()
        pin14Label.setBuddy(self.pin14LineEdit)
    
        pin15Label = Qt.QLabel("15 (A1)")
        self.pin15LineEdit = Qt.QLineEdit()
        pin15Label.setBuddy(self.pin15LineEdit)

        pin16Label = Qt.QLabel("16 (A2)")
        self.pin16LineEdit = Qt.QLineEdit()
        pin16Label.setBuddy(self.pin16LineEdit)

        pin17Label = Qt.QLabel("17 (A3)")
        self.pin17LineEdit = Qt.QLineEdit()
        pin17Label.setBuddy(self.pin17LineEdit)

        pin18Label = Qt.QLabel("18 (A4)")
        self.pin18LineEdit = Qt.QLineEdit()
        pin18Label.setBuddy(self.pin18LineEdit)

        pin19Label = Qt.QLabel("19 (A5)")
        self.pin19LineEdit = Qt.QLineEdit()
        pin19Label.setBuddy(self.pin19LineEdit)

        self.pshBtn1 = Qt.QPushButton(self.tr("CLEAR"))
        self.pshBtn1.clicked.connect(self.clear_pins)

        self.pshBtn2 = Qt.QPushButton(self.tr("EXPORT"))
        self.pshBtn2.clicked.connect(self.export_pins)
    
        self.pshBtn3 = Qt.QPushButton(self.tr("LOAD"))   
        self.pshBtn3.clicked.connect(self.load_pins)
    
        self.pshBtn4 = Qt.QPushButton(self.tr("BUILD"))
        self.pshBtn4.clicked.connect(self.build_pins)
        
        #self.registerField("Built?*", self.pshBtn4)    

        layout = Qt.QGridLayout()
        layout.addWidget(dpinsLabel1, 0, 0)
        layout.addWidget(dpinsLabel2, 0, 1)
        layout.addWidget(pin2Label, 1, 0)
        layout.addWidget(self.pin2LineEdit, 1, 1)
        layout.addWidget(pin3Label, 2, 0)
        layout.addWidget(self.pin3LineEdit, 2, 1)
        layout.addWidget(pin4Label, 3, 0)
        layout.addWidget(self.pin4LineEdit, 3, 1)
        layout.addWidget(pin5Label, 4, 0)
        layout.addWidget(self.pin5LineEdit, 4, 1) 
        layout.addWidget(pin6Label, 5, 0)
        layout.addWidget(self.pin6LineEdit, 5, 1)
        layout.addWidget(pin7Label, 6, 0)
        layout.addWidget(self.pin7LineEdit, 6, 1)        
        layout.addWidget(pin8Label, 7, 0)
        layout.addWidget(self.pin8LineEdit, 7, 1)
        layout.addWidget(pin9Label, 8, 0)
        layout.addWidget(self.pin9LineEdit, 8, 1)      
        layout.addWidget(pin10Label, 9, 0)
        layout.addWidget(self.pin10LineEdit, 9, 1)
        layout.addWidget(pin11Label, 10, 0)
        layout.addWidget(self.pin11LineEdit, 10, 1) 
        layout.addWidget(pin12Label, 11, 0)
        layout.addWidget(self.pin12LineEdit, 11, 1)
        layout.addWidget(apinsLabel1, 12, 0)
        layout.addWidget(apinsLabel2, 12, 1)        
        layout.addWidget(pin14Label, 13, 0)
        layout.addWidget(self.pin14LineEdit, 13, 1)       
        layout.addWidget(pin15Label, 14, 0)
        layout.addWidget(self.pin15LineEdit, 14, 1)           
        layout.addWidget(pin16Label, 15, 0)
        layout.addWidget(self.pin16LineEdit, 15, 1)           
        layout.addWidget(pin17Label, 16, 0)
        layout.addWidget(self.pin17LineEdit, 16, 1)            
        layout.addWidget(pin18Label, 17, 0)
        layout.addWidget(self.pin18LineEdit, 17, 1)          
        layout.addWidget(pin19Label, 18, 0)
        layout.addWidget(self.pin19LineEdit, 18, 1)     
            
        layout2 = Qt.QHBoxLayout()
        layout2.addWidget(self.pshBtn1)
        layout2.addWidget(self.pshBtn3)
        layout2.addWidget(self.pshBtn4)
        layout2.addWidget(self.pshBtn2)
    
        layout.addLayout(layout2, 19, 1)
    
        self.setLayout(layout)

        self.LineEdits = [self.pin2LineEdit, self.pin3LineEdit, self.pin4LineEdit, self.pin5LineEdit, self.pin6LineEdit, self.pin7LineEdit, self.pin8LineEdit, 
                          self.pin9LineEdit, self.pin10LineEdit, self.pin11LineEdit, self.pin12LineEdit, self.pin14LineEdit, self.pin15LineEdit, self.pin16LineEdit,
                          self.pin17LineEdit, self.pin18LineEdit, self.pin19LineEdit]
    
        self.pinsnums = [2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19]
        
        def nextId(self):
            return ArduinoWizard.MethodsPage

class MethodsPage(Qt.QWizardPage):
    def compile_code(self):
        global assu, setu, loopu, resu
        assu = self.txtEdt1.toPlainText()
        setu = self.txtEdt2.toPlainText()
        loopu = self.txtEdt3.toPlainText()
        resu = OrderedDict()
        for line, key in zip(setu.splitlines(), assu.splitlines()):
            if 'INPUT' in line:
                resu[''.join(c for c in key if c.isdigit())] = deque()
        
    def autofill_pin_assigns(self):
        global pins
        self.txtEdt1.clear()
        self.txtEdt2.clear()
        self.txtEdt3.clear()
        for key in pins.keys():
            self.txtEdt1.append(pins[key][0] + '=' + key)
            if pins[key][1] == 'INPUT':
                self.txtEdt2.append('a.pinMode(%s, a.INPUT)' % str(pins[key][0]))
            elif pins[key][1] == 'OUTPUT':
                self.txtEdt2.append('a.pinMode(%s, a.OUTPUT)' % str(pins[key][0]))
    
    def __init__(self, parent=None):
                 
        super(MethodsPage, self).__init__(parent)

        self.setTitle(self.tr("Program the Arduino!"))
        self.setSubTitle(self.tr("Define setup and loop voids for Arduino"))
 
        pshBtn1 = Qt.QPushButton(self.tr("Autofill Pin Assignments"))
        pshBtn1.clicked.connect(self.autofill_pin_assigns)
      
        self.txtEdt1 = Qt.QTextEdit()
       
        self.txtEdt2 = Qt.QTextEdit()

        self.txtEdt3 = Qt.QTextEdit()
        
        pshBtn2 = Qt.QPushButton(self.tr("Compile Code"))
        pshBtn2.clicked.connect(self.compile_code)

        layout = Qt.QVBoxLayout(self)
        layout.addWidget(pshBtn1)
        layout.addWidget(self.txtEdt1)
        layout.addWidget(self.txtEdt2)
        layout.addWidget(self.txtEdt3)
        layout.addWidget(pshBtn2)
                            
    def nextId(self):
        return -1
       


# main ============================================================================================================================================================================

def main():
    import sys

    app = Qt.QApplication(sys.argv)
    awiz = ArduinoWizard()
    awiz.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()











