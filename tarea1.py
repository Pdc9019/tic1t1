from gpiozero import LED, Button, Buzzer
from time import sleep
from random import choice
from signal import pause

# Configuración de los GPIO para LEDs (dos pines por LED), botones y buzzer
led_pins = [
    (20, 21),  # LED 1
    (16, 12),  # LED 2
    (26, 19),  # LED 3
    (13, 6),   # LED 4
    (5, 24)    # LED 5
]

button_pins = [4, 17, 18, 27, 22]  # Botones 1 a 5
buzzer_pin = 23                    # Parlante/buzzer

# Crear instancias de LEDs y botones
leds = [(LED(pin1), LED(pin2)) for pin1, pin2 in led_pins]
buttons = [Button(pin) for pin in button_pins]
buzzer = Buzzer(buzzer_pin)

# Configuración inicial del juego
num_jugadores = int(input("Ingrese el número de jugadores: "))
puntajes = [0] * num_jugadores
num_rondas = int(input("Ingrese el número de rondas: "))
tiempo_turno = int(input("Ingrese el tiempo entre cada turno (segundos): "))
tiempo_entre_leds = int(input("Ingrese el tiempo entre cada combinación de LEDs (segundos): "))

def inicio_juego():
    buzzer.beep(on_time=0.5, off_time=0.5, n=3)
    sleep(2)

def jugar_ronda(jugador):
    print(f"Turno del Jugador {jugador + 1}")
    for ronda in range(num_rondas):
        print(f"Ronda {ronda + 1}")
        secuencia = generar_secuencia()
        for led_pair, boton in zip(secuencia, buttons):
            if any(led.is_lit for led in led_pair):
                apagar_leds(led_pair)
            else:
                encender_leds(led_pair)
            sleep(tiempo_entre_leds)

        for boton in buttons:
            boton.when_pressed = lambda: verificar_acierto(boton, leds, jugador)

        sleep(tiempo_turno)

def generar_secuencia():
    secuencia = []
    for led_pair in leds:
        estado = choice([True, False])
        if estado:
            encender_leds(led_pair)
        else:
            apagar_leds(led_pair)
        secuencia.append(led_pair)
    return secuencia

def encender_leds(led_pair):
    for led in led_pair:
        led.on()

def apagar_leds(led_pair):
    for led in led_pair:
        led.off()

def verificar_acierto(boton, leds, jugador):
    indice = buttons.index(boton)
    if any(led.is_lit for led in leds[indice]):
        apagar_leds(leds[indice])
        buzzer.beep(on_time=0.2, n=1)
        puntajes[jugador] += 1
        print(f"Jugador {jugador + 1} acierta!")
    else:
        buzzer.beep(on_time=0.2, off_time=0.1, n=2)
        puntajes[jugador] -= 1
        print(f"Jugador {jugador + 1} falla!")

# Inicia el juego
inicio_juego()

for jugador in range(num_jugadores):
    jugar_ronda(jugador)

print("Juego terminado!")
print("Puntajes finales:", puntajes)

# Limpieza
for led_pair in leds:
    apagar_leds(led_pair)
buzzer.off()

pause()
