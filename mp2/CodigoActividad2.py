import sys
import os
import time
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import RPi.GPIO as GPIO

# Configuración de GPIO
GPIO.setmode(GPIO.BCM)
LED1_PIN = 20
LED1_GND = 21
LED2_PIN = 16
LED2_GND = 26

GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(LED1_GND, GPIO.OUT)
GPIO.setup(LED2_GND, GPIO.OUT)
GPIO.output(LED1_GND, GPIO.LOW)
GPIO.output(LED2_GND, GPIO.LOW)

pwm_led = GPIO.PWM(LED2_PIN, 1000)  # PWM para el control de brillo en el LED 2
pwm_led.start(0)  # Iniciar el LED en 0% de brillo

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de LED y Temporizador")
        self.resize(800, 600)
        
        self.led1_status = False
        self.timer_active = False
        self.timer_countdown = 5
        self.image_index = 0
        
        # Lista de textos descriptivos
        self.text_list = [
            "Ampolleta Encendida", "Ampolleta Apagada", "Lucario", 
            "Vamo' a Calmarnos XDD", "Charmander", "Pikachu", 
            "Pokeball", "Mew", "Eevee", "Psyduck"
        ]
        
        # Configuración de widgets
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Botón para encender/apagar LED1
        self.LED1Switch = QPushButton("Primer LED On / Off", self.centralwidget)
        self.LED1Switch.setGeometry(40, 350, 200, 50)
        self.LED1Switch.clicked.connect(self.toggle_led1)

        # Dial para el brillo del LED2
        self.LED2BrightnessDial = QDial(self.centralwidget)
        self.LED2BrightnessDial.setGeometry(260, 350, 100, 100)
        self.LED2BrightnessDial.setRange(0, 100)
        self.LED2BrightnessDial.valueChanged.connect(self.change_led2_brightness)
        
        # Botón para iniciar/detener temporizador
        self.TimerSwitch = QPushButton("Temporizador Cambio Imágenes On / Off", self.centralwidget)
        self.TimerSwitch.setGeometry(580, 140, 181, 131)
        self.TimerSwitch.clicked.connect(self.toggle_timer)
        
        # Temporizador LCD
        self.Timer = QLCDNumber(self.centralwidget)
        self.Timer.setGeometry(580, 60, 181, 51)
        self.Timer.display(self.timer_countdown)
        
        # Labels para mostrar imagen y texto
        self.PicLabel = QLabel(self.centralwidget)
        self.PicLabel.setGeometry(40, 60, 200, 200)
        self.TextLabel = QLabel(self.centralwidget)
        self.TextLabel.setGeometry(260, 60, 200, 200)
        
        # Cargar primera imagen y texto
        self.update_image_text()

        # Temporizador de cuenta regresiva
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_timer)

    def toggle_led1(self):
        """Enciende y apaga el primer LED."""
        self.led1_status = not self.led1_status
        GPIO.output(LED1_PIN, GPIO.HIGH if self.led1_status else GPIO.LOW)

    def change_led2_brightness(self, value):
        """Ajusta el brillo del segundo LED."""
        pwm_led.ChangeDutyCycle(value)

    def toggle_timer(self):
        """Inicia o detiene el temporizador de cambio de imágenes."""
        self.timer_active = not self.timer_active
        if self.timer_active:
            self.countdown_timer.start(1000)  # Temporizador de cuenta regresiva en segundos
        else:
            self.countdown_timer.stop()
            self.timer_countdown = 5  # Reinicia el temporizador a 5 segundos
            self.Timer.display(self.timer_countdown)

    def update_timer(self):
        """Actualiza la cuenta regresiva del temporizador."""
        if self.timer_countdown > 0:
            self.timer_countdown -= 1
            self.Timer.display(self.timer_countdown)
        else:
            self.timer_countdown = 5
            self.Timer.display(self.timer_countdown)
            self.update_image_text()

    def update_image_text(self):
        """Cambia la imagen y el texto al siguiente en la lista."""
        self.image_index = (self.image_index + 1) % 10
        image_path = f"pic{self.image_index}.png"
        
        if os.path.exists(image_path):
            self.PicLabel.setPixmap(QPixmap(image_path).scaled(200, 200))
        
        self.TextLabel.setText(self.text_list[self.image_index])

    def closeEvent(self, event):
        """Limpia los recursos de GPIO al cerrar la aplicación."""
        GPIO.cleanup()
        pwm_led.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
