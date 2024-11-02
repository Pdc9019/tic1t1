import paramiko
import time
import pandas as pd
import matplotlib.pyplot as plt
import json

# Datos de conexión SSH
raspi_host = '192.168.1.42'
raspi_port = 22
raspi_user = 'raspi'
raspi_password = 'raspi'
remote_file_path = '/home/raspi/tic1t1/mp2/sensor_data.log'
local_file_path = 'sensor_data_local.log'
alert_file_path = 'alert_status.json'

# Umbrales de alerta
temperature_threshold = {'low': 15.0, 'high': 30.0}
humidity_threshold = {'low': 30.0, 'high': 70.0}
distance_threshold = {'low': 0.5, 'high': 2.0}

# Establecer conexión SSH
def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(raspi_host, port=raspi_port, username=raspi_user, password=raspi_password)
    return client

# Descargar el archivo de logging actualizado
def download_log_file(ssh_client):
    sftp = ssh_client.open_sftp()
    sftp.get(remote_file_path, local_file_path)
    sftp.close()

# Cargar datos desde el archivo de logging
def load_data():
    try:
        # Leer el archivo de logging y cargarlo en un DataFrame
        data = pd.read_csv(local_file_path, delimiter=',', header=None, names=['Datetime', 'Temperature_C', 'Humidity', 'Distance'])
        
        # Convertir la columna 'Datetime' a un tipo datetime de pandas
        data['Datetime'] = pd.to_datetime(data['Datetime'], format='%m/%d/%Y %H:%M:%S')

        return data
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

# Función para mostrar un gráfico de los datos disponibles
def show_graph():
    data = load_data()
    if data is None or data.empty:
        print("No hay datos para mostrar.")
        return

    # Graficar los datos disponibles
    plt.figure(figsize=(19.2, 10.8))
    plt.subplot(3,1,1)
    plt.plot(data['Datetime'], data['Temperature_C'], label='Temperature (C)', color='blue')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura')
    plt.grid('on')

    plt.subplot(3,1,2)
    plt.plot(data['Datetime'], data['Humidity'], label='Humidity (%)', color='orange')
    plt.ylabel('Humedad')
    plt.title('Humedad')
    plt.grid('on')

    plt.subplot(3,1,3)
    plt.plot(data['Datetime'], data['Distance'], label='Distance (m)', color='green')
    plt.xlabel('Datetime')
    plt.ylabel('Distancia (m)')
    plt.title('Distancia')
    plt.grid('on')

    plt.show()

# Función para mostrar un resumen de los últimos 5 minutos
def show_summary():
    data = load_data()
    if data is None or data.empty:
        print("No hay datos para mostrar.")
        return

    # Filtrar datos de los últimos 5 minutos
    last_5_minutes = data[data['Datetime'] > (pd.Timestamp.now() - pd.Timedelta(minutes=5))]
    if last_5_minutes.empty:
        print("No hay datos disponibles en los últimos 5 minutos.")
        return

    # Mostrar valores mínimos, máximos y promedio de los últimos 5 minutos
    summary = last_5_minutes[['Temperature_C', 'Humidity', 'Distance']].agg(['min', 'max', 'mean'])
    print(summary)

# Función para enviar alerta a la Raspberry Pi
def send_alert(ssh_client):
    data = load_data()
    if data is None or data.empty:
        print("No hay datos para generar una alerta.")
        return

    # Filtrar datos de los últimos 5 minutos
    last_5_minutes = data[data['Datetime'] > (pd.Timestamp.now() - pd.Timedelta(minutes=5))]
    if last_5_minutes.empty:
        print("No hay datos disponibles en los últimos 5 minutos.")
        return

    # Calcular el promedio de cada variable
    averages = last_5_minutes[['Temperature_C', 'Humidity', 'Distance']].mean()

    # Generar alerta
    alert_status = {
        "Temp": "LOW" if averages['Temperature_C'] < temperature_threshold['low'] else "HIGH" if averages['Temperature_C'] > temperature_threshold['high'] else "NORMAL",
        "Hum": "LOW" if averages['Humidity'] < humidity_threshold['low'] else "HIGH" if averages['Humidity'] > humidity_threshold['high'] else "NORMAL",
        "Dist": "LOW" if averages['Distance'] < distance_threshold['low'] else "HIGH" if averages['Distance'] > distance_threshold['high'] else "NORMAL"
    }

    # Guardar alerta en un archivo JSON
    with open(alert_file_path, 'w') as alert_file:
        json.dump(alert_status, alert_file)

    # Enviar el archivo de alerta a la Raspberry Pi
    sftp = ssh_client.open_sftp()
    sftp.put(alert_file_path, f'/home/raspi/tic1t1/mp2/{alert_file_path}')
    sftp.close()
    print("Alerta enviada correctamente.")

# Función para quitar la alerta en la Raspberry Pi
def clear_alert(ssh_client):
    # Generar un estado de alerta "NORMAL" para todas las variables
    alert_status = {
        "Temp": "NORMAL",
        "Hum": "NORMAL",
        "Dist": "NORMAL"
    }

    # Guardar el estado de alerta en un archivo JSON
    with open(alert_file_path, 'w') as alert_file:
        json.dump(alert_status, alert_file)

    # Enviar el archivo de alerta a la Raspberry Pi
    sftp = ssh_client.open_sftp()
    sftp.put(alert_file_path, f'/home/raspi/tic1t1/mp2/{alert_file_path}')
    sftp.close()
    print("Alerta eliminada correctamente.")

# Menú de selección para el usuario
def main():
    ssh_client = ssh_connect()

    try:
        while True:
            # Descargar el archivo de logging actualizado
            download_log_file(ssh_client)

            # Mostrar el menú al usuario
            print("\nSeleccione una opción:")
            print("1. Mostrar gráfico de los datos disponibles")
            print("2. Mostrar resumen de los últimos 5 minutos")
            print("3. Enviar alerta a Raspberry Pi")
            print("4. Quitar alerta en Raspberry Pi")
            print("5. Salir")
            choice = input("Ingrese su elección: ")

            if choice == '1':
                show_graph()
            elif choice == '2':
                show_summary()
            elif choice == '3':
                send_alert(ssh_client)
            elif choice == '4':
                clear_alert(ssh_client)

            elif choice == '5':
                break
            else:
                print("Opción inválida. Por favor, intente nuevamente.")

            # Pausa breve para evitar que el menú se repita muy rápido
            time.sleep(1)
    finally:
        ssh_client.close()

if __name__ == "__main__":
    main()
