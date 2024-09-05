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

def encender_led(led_pair, color):
    """Enciende un LED en un color específico (rojo o azul)."""
    if color == "azul":
        GPIO.output(led_pair[0], GPIO.HIGH)
        GPIO.output(led_pair[1], GPIO.LOW)
    elif color == "rojo":
        GPIO.output(led_pair[0], GPIO.LOW)
        GPIO.output(led_pair[1], GPIO.HIGH)

def apagar_leds(led_pair):
    """Apaga ambos colores del LED."""
    GPIO.output(led_pair[0], GPIO.LOW)
    GPIO.output(led_pair[1], GPIO.LOW)

def beep_buzzer(tiempo):
    """Emite un sonido por el buzzer."""
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(tiempo)
    GPIO.output(buzzer_pin, GPIO.LOW)

def inicio_juego():
    """Emite un tono para iniciar el juego."""
    beep_buzzer(0.5)
    time.sleep(0.5)
    beep_buzzer(0.5)
    time.sleep(0.5)
    beep_buzzer(0.5)

def generar_secuencia():
    """Genera una secuencia aleatoria de LEDs con zonas de acierto y trampa."""
    secuencia = []
    for led_pair in led_pins:
        color = random.choice(["rojo", "azul"])
        encender_led(led_pair, color)
        secuencia.append(color)
    return secuencia

def verificar_acierto(indice, secuencia, jugador):
    """Verifica si el jugador acertó o falló al presionar un botón."""
    if secuencia[indice] == "azul":
        apagar_leds(led_pins[indice])  # Apaga el LED si se acierta
        beep_buzzer(0.2)  # Sonido de acierto
        print(f"Jugador {jugador + 1} acertó en LED {indice + 1} (zona de acierto)")
        return 1
    else:
        print(f"Jugador {jugador + 1} falló en LED {indice + 1} (zona de trampa)")
        # Emite un sonido diferente para indicar que falló
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

try:
    inicio_juego()

    for jugador in range(num_jugadores):
        print(f"Turno del Jugador {jugador + 1}")
        for ronda in range(num_rondas):
            print(f"Ronda {ronda + 1}")
            secuencia = generar_secuencia()

            inicio_ronda = time.time()
            while time.time() - inicio_ronda < tiempo_turno:
                for i, pin in enumerate(button_pins):
                    if GPIO.input(pin) == GPIO.HIGH:  # Si se presiona el botón
                        resultado = verificar_acierto(i, secuencia, jugador)
                        puntajes[jugador] += resultado
                        time.sleep(0.5)  # Evitar múltiples lecturas del mismo botón

                time.sleep(tiempo_entre_leds)

            print(f"Jugador {jugador + 1} puntaje: {puntajes[jugador]}")

    print("Juego terminado!")
    print("Puntajes finales:", puntajes)

finally:
    # Apagamos todos los LEDs y limpiamos la configuración GPIO
    for led_pair in led_pins:
        apagar_leds(led_pair)
    GPIO.cleanup()
