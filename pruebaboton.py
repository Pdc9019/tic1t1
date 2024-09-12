import RPi.GPIO as GPIO
import time

# Configuración de los GPIO para LEDs, botones y buzzer
led_pins = [
    (20, 21),  # LED 1
    (16, 12),  # LED 2
    (26, 19),  # LED 3
    (13, 6),   # LED 4
    (5, 24)    # LED 5
]
button_pins = [4, 17, 18, 27, 22]  # Botones 1 a 5
buzzer_pin = 23  # Parlante/buzzer

# Configuración de pines GPIO
GPIO.setmode(GPIO.BCM)

# Configuramos los LEDs como salidas
for led_pair in led_pins:
    GPIO.setup(led_pair[0], GPIO.OUT)
    GPIO.setup(led_pair[1], GPIO.OUT)

# Configuramos los botones como entradas con pull-down resistors
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuramos el buzzer como salida
GPIO.setup(buzzer_pin, GPIO.OUT)

def encender_led(led_pair):
    """Enciende ambos colores del LED."""
    GPIO.output(led_pair[0], GPIO.HIGH)
    GPIO.output(led_pair[1], GPIO.HIGH)

def apagar_led(led_pair):
    """Apaga ambos colores del LED."""
    GPIO.output(led_pair[0], GPIO.LOW)
    GPIO.output(led_pair[1], GPIO.LOW)

def beep_buzzer(tiempo):
    """Emite un sonido por el buzzer."""
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(tiempo)
    GPIO.output(buzzer_pin, GPIO.LOW)

# Bucle principal
try:
    while True:
        for i, button_pin in enumerate(button_pins):
            if GPIO.input(button_pin) == GPIO.HIGH:  # Si se presiona el botón
                encender_led(led_pins[i])  # Enciende el LED correspondiente
                beep_buzzer(0.2)  # Suena el buzzer
            else:
                apagar_led(led_pins[i])  # Apaga el LED cuando el botón se suelta

        time.sleep(0.1)  # Pequeño retardo para evitar sobrecarga del CPU

except KeyboardInterrupt:
    print("Saliendo del programa...")
finally:
    # Limpieza de configuración GPIO al salir
    GPIO.cleanup()
