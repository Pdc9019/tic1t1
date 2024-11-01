import time
import board
import adafruit_dht
from gpiozero import DistanceSensor, LED, Buzzer
import subprocess
import logging
from datetime import datetime
import json

# Configuración del archivo de logging
logging.basicConfig(
    filename='sensor_data.log',
    level=logging.INFO,
    format='%(asctime)s, %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S'
)

script_path = '/home/raspi/tic1t1/mp2/correct_sensor.sh'
result = subprocess.run([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

sensor = DistanceSensor(24, 23, max_distance=3, threshold_distance=0.2)
dhtDevice = adafruit_dht.DHT11(board.D18)

# Configuración de LEDs y buzzer
led_temp_1 = LED(4)
led_temp_2 = LED(25)

led_hum_1 = LED(17)
led_hum_2 = LED(27)
led_hum_3 = LED(22)

led_dist_1 = LED(19)
led_dist_2 = LED(13)

buzzer_1 = Buzzer(5)
buzzer_2 = Buzzer(6)

alert_file_path = '/home/raspi/tic1t1/mp2/alert_status.json'

# Funciones para manejar LEDs y buzzer
def actualizar_leds(alert_status):
    # Temperatura
    if alert_status["Temp"] == "LOW":
        led_temp_1.off()
        led_temp_2.on()  # Azul
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de temperatura: LOW")
    elif alert_status["Temp"] == "HIGH":
        led_temp_1.on()  # Rojo
        led_temp_2.off()
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de temperatura: HIGH")
    else:
        led_temp_1.off()
        led_temp_2.off()  # Verde (simulado apagando LEDs)
        buzzer_1.off()
        buzzer_2.off()
    
    # Humedad
    if alert_status["Hum"] == "LOW":
        led_hum_1.off()
        led_hum_2.off()
        led_hum_3.on()  # Azul
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de humedad: LOW")
    elif alert_status["Hum"] == "HIGH":
        led_hum_1.on()  # Rojo
        led_hum_2.off()
        led_hum_3.off()
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de humedad: HIGH")
    else:
        led_hum_1.off()
        led_hum_2.off()
        led_hum_3.off()  # Verde (simulado apagando LEDs)
        buzzer_1.off()
        buzzer_2.off()
    
    # Distancia
    if alert_status["Dist"] == "LOW":
        led_dist_1.off()
        led_dist_2.on()  # Azul
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de distancia: LOW")
    elif alert_status["Dist"] == "HIGH":
        led_dist_1.on()  # Rojo
        led_dist_2.off()
        buzzer_1.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        buzzer_2.beep(on_time=0.2, off_time=0.8, n=3, background=True)
        print("Alerta de distancia: HIGH")
    else:
        led_dist_1.off()
        led_dist_2.off()  # Verde (simulado apagando LEDs)
        buzzer_1.off()
        buzzer_2.off()

while True:
    try:
        # Leer distancia y redondear a 3 decimales
        distance = round(sensor.distance, 3)
        
        # Leer temperatura y humedad
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # Comprobar si los valores son válidos antes de escribirlos
        if temperature_c is not None and humidity is not None:
            # Guardar los datos en el archivo de logging en formato numérico
            logging.info(f"{temperature_c:.3f}, {humidity:.3f}, {distance:.3f}")
            print(f"Time: {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}, Temperature: {temperature_c:.3f} C, Humidity: {humidity:.3f}%, Distance: {distance:.3f} m")

        # Leer el archivo de alertas JSON
        try:
            with open(alert_file_path, 'r') as alert_file:
                alert_status = json.load(alert_file)
                actualizar_leds(alert_status)
        except FileNotFoundError:
            print("Archivo de alerta no encontrado. Esperando próxima actualización.")

    except RuntimeError as error:
        # Errores durante la lectura del sensor
        error_message = f"Runtime error: {error.args[0]}"
        logging.error(f"[Error]: {error_message}")
        time.sleep(2.0)
        continue
    except Exception as error:
        # Otras excepciones
        error_message = f"Unexpected error: {error}"
        logging.critical(f"[Critical]: {error_message}")
        raise error

    # Intervalo de tiempo entre lecturas
    time.sleep(2.0)

if dhtDevice:
    dhtDevice.exit()
