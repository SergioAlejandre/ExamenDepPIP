import sys
from PyQt5 import uic, QtWidgets, QtCore
import serial as placa

qtCreatorFile = "Examen.ui"
Ui_MainWindow, _ = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.arduino = None
        self.btn_accion.clicked.connect(self.accion)

        self.segundoPlano = QtCore.QTimer()
        self.segundoPlano.timeout.connect(self.lecturas)

    def lecturas(self):
        if self.arduino and self.arduino.isOpen():
            if self.arduino.inWaiting():
                try:
                    lectura = self.arduino.readline().decode().strip()
                    if lectura != "":
                        valor_ldr = int(lectura)
                        self.lista_datos.addItem(f"Valor LDR: {valor_ldr}")
                        self.lista_datos.setCurrentRow(self.lista_datos.count() - 1)

                        led0_encendido = valor_ldr < 400
                        led1_encendido = valor_ldr < 300

                        self.btn_led0.setText("Encendido" if led0_encendido else "Apagado")
                        self.btn_led1.setText("Encendido" if led1_encendido else "Apagado")
                except ValueError as e:
                    pass

    def accion(self):
        try:
            texto = self.btn_accion.text().upper()
            if texto == "CONECTAR":
                com = "COM" + self.txt_com.text()
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("CONECTADO")
                self.arduino = placa.Serial(com, baudrate=9600, timeout=1)
                self.segundoPlano.start(100)
            elif texto == "DESCONECTAR":
                self.btn_accion.setText("RECONECTAR")
                self.txt_estado.setText("DESCONECTADO")
                self.segundoPlano.stop()
                if self.arduino:
                    self.arduino.close()
            else:
                self.btn_accion.setText("DESCONECTAR")
                self.txt_estado.setText("RECONECTADO")
                if self.arduino:
                    self.arduino.open()
                self.segundoPlano.start(100)
        except Exception as error:
            self.txt_estado.setText("ERROR")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())