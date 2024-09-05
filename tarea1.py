import RPi.GPIO as GPIO
import time
import random

# Configuración de los GPIO para LEDs de dos colores, botones y buzzer
led_pins = [
    (20, 21),  # LED 1
    (16, 12),  # LED 2
    (26, 19),  # LED 3
    (13, 6),   # LED 4
    (5, 24)    # LED 5
]
button_pins = [4, 17, 18, 27, 22]  # Botones 1 a 5
buzzer_pin = 23                    # Parlante/buzzer

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

# Funciones para encender y apagar LEDs
def encender_led(led_pair, color):
    if color == "azul":
        GPIO.output(led_pair[0], GPIO.HIGH)
        GPIO.output(led_pair[1], GPIO.LOW)
    elif color == "rojo":
        GPIO.output(led_pair[0], GPIO.LOW)
        GPIO.output(led_pair[1], GPIO.HIGH)

def apagar_leds(led_pair):
    GPIO.output(led_pair[0], GPIO.LOW)
    GPIO.output(led_pair[1], GPIO.LOW)

# Función para hacer sonar el buzzer
def beep_buzzer(tiempo):
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(tiempo)
    GPIO.output(buzzer_pin, GPIO.LOW)

# Iniciar juego
def inicio_juego():
    beep_buzzer(0.5)
    time.sleep(0.5)
    beep_buzzer(0.5)
    time.sleep(0.5)
    beep_buzzer(0.5)

# Generar secuencia aleatoria de LEDs (aciertos y trampas)
def generar_secuencia():
    secuencia = []
    for led_pair in led_pins:
        color = random.choice(["rojo", "azul"])
        encender_led(led_pair, color)
        secuencia.append(color)
    return secuencia

# Verificar acierto o fallo al presionar un botón
def verificar_acierto(indice, secuencia, jugador):
    if secuencia[indice] == "azul":  # Acierto
        apagar_leds(led_pins[indice])
        beep_buzzer(0.2)  # Sonido de acierto
        return 1
    else:  # Falla
        beep_buzzer(0.2)
        time.sleep(0.1)
        beep_buzzer(0.2)  # Sonido de fallo
        return -1

# Configuración inicial del juego
num_jugadores = int(input("Ingrese el número de jugadores: "))
puntajes = [0] * num_jugadores
num_rondas = int(input("Ingrese el número de rondas: "))
tiempo_turno = float(input("Ingrese el tiempo entre cada turno (segundos): "))
tiempo_entre_leds = float(input("Ingrese el tiempo entre cada combinación de LEDs (segundos): "))

# Agregar debounce para evitar múltiples lecturas en una sola pulsación
def manejar_pulsacion(pin):
    for i, boton_pin in enumerate(button_pins):
        if pin == boton_pin:
            resultado = verificar_acierto(i, secuencia, jugador_actual)
            puntajes[jugador_actual] += resultado

try:
    inicio_juego()

    for jugador_actual in range(num_jugadores):
        print(f"Turno del Jugador {jugador_actual + 1}")
        for ronda in range(num_rondas):
            print(f"Ronda {ronda + 1}")
            secuencia = generar_secuencia()

            inicio_ronda = time.time()

            # Configurar el evento de pulsación para cada botón
            for pin in button_pins:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=manejar_pulsacion, bouncetime=200)

            # Mantener el juego activo durante el tiempo del turno
            while time.time() - inicio_ronda < tiempo_turno:
                time.sleep(0.01)  # Evitar uso excesivo de CPU

            # Desactivar el evento de pulsación una vez que termina el turno
            for pin in button_pins:
                GPIO.remove_event_detect(pin)

            print(f"Jugador {jugador_actual + 1} puntaje: {puntajes[jugador_actual]}")

    print("Juego terminado!")
    print("Puntajes finales:", puntajes)

finally:
    # Apagar todos los LEDs y limpiar los pines GPIO
    for led_pair in led_pins:
        apagar_leds(led_pair)
    GPIO.cleanup()
