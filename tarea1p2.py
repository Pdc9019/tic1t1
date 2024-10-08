import RPi.GPIO as GPIO
import time
import random

# Configuración de los GPIO para LEDs de dos colores, botones y buzzer
led_pins = [
    (21, 20),  # LED 1
    (12, 16),  # LED 2
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
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Configuramos el buzzer como salida
GPIO.setup(buzzer_pin, GPIO.OUT)

# Secuencias predefinidas de LEDs en rojo (zonas de trampa)
secuencias_predefinidas = [
    ["rojo", "verde", "rojo", "verde", "rojo"],  # Secuencia 1
    ["verde", "rojo", "verde", "rojo", "verde"],  # Secuencia 2
    ["rojo", "rojo", "verde", "verde", "rojo"],  # Secuencia 3
    ["verde", "verde", "rojo", "rojo", "verde"],  # Secuencia 4
]
sec_ant = None


def encender_led(led_pair, color):
    """Enciende un LED en un color específico (rojo o verde)."""
if color == "verde":
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
    beep_buzzer(0.8)

def seleccionar_secuencia():
    global sec_ant
    """Selecciona aleatoriamente una de las secuencias predefinidas."""
    if sec_ant is None:
        sec_ant = random.choice(secuencias_predefinidas)
        return sec_ant
    while True:
        sec_new = random.choice(secuencias_predefinidas)
        if sec_ant != sec_new:
            sec_ant = sec_new
            return sec_new   
        

def aplicar_bonificacion(aciertos_consecutivos):
    """Aplica bonificaciones según los aciertos consecutivos."""
    if aciertos_consecutivos >= 32:
        return 8
    elif aciertos_consecutivos >= 16:
        return 5
    elif aciertos_consecutivos >= 8:
        return 3
    elif aciertos_consecutivos >= 4:
        return 2
    else:
        return 0

def verificar_acierto(indice, secuencia, jugador, aciertos_consecutivos):
    """Verifica si el jugador acertó o falló al presionar un botón."""
    if secuencia[indice] == "verde":
        apagar_leds(led_pins[indice])  # Apaga el LED si se acierta
        beep_buzzer(0.2)  # Sonido de acierto
        aciertos_consecutivos += 1
        print(f"Jugador {jugador + 1} acertó en LED {indice + 1} (zona de acierto)")
        return 1 + aplicar_bonificacion(aciertos_consecutivos), aciertos_consecutivos
    else:
        print(f"Jugador {jugador + 1} falló en LED {indice + 1} (zona de trampa)")
        beep_buzzer(0.2)
        time.sleep(0.1)
        beep_buzzer(0.2)  # Sonido de fallo
        aciertos_consecutivos = 0
        return -1, aciertos_consecutivos


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
        aciertos_consecutivos = 0  # Contador de aciertos consecutivos
        for ronda in range(num_rondas):
            print(f"Ronda {ronda + 1}")
            
            inicio_ronda = time.time()
            while time.time() - inicio_ronda < tiempo_turno:
                # Selecciona una nueva secuencia aleatoria durante el turno
                secuencia = seleccionar_secuencia()
                print(f"Secuencia seleccionada: {secuencia}")
                
                # Enciende los LEDs según la secuencia
                for i, color in enumerate(secuencia):
                    encender_led(led_pins[i], color)

                # Monitorea los botones durante el tiempo del turno
                tiempo_secuencia = time.time()
                while time.time() - tiempo_secuencia < tiempo_entre_leds:
                    for i, pin in enumerate(button_pins):
                        if GPIO.input(pin) == GPIO.LOW:  # Si se presiona el botón
                            resultado, aciertos_consecutivos = verificar_acierto(i, secuencia, jugador, aciertos_consecutivos)
                            puntajes[jugador] += resultado
                            time.sleep(0.01)  # Evitar múltiples lecturas del mismo botón

            print(f"Jugador {jugador + 1} puntaje: {puntajes[jugador]}")

    print("Juego terminado!")
    print("Puntajes finales:", puntajes)

finally:
    # Apagamos todos los LEDs y limpiamos la configuración GPIO
    for led_pair in led_pins:
        apagar_leds(led_pair)
    GPIO.cleanup()
