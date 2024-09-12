import RPi.GPIO as GPIO
import time

button_pins = [4, 17, 18, 27, 22]  # Botones 1 a 5

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)



# Configuramos los botones como entradas con pull-down resistors
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Bucle principal

while True:
    for i, button_pin in enumerate(button_pins):
        if GPIO.input(button_pin) == GPIO.LOW:  # Si se presiona el botón
            print('hola '+ str(button_pin))


    time.sleep(0.1)  # Pequeño retardo para evitar sobrecarga del CPU

GPIO.cleanup()
