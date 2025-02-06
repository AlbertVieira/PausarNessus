import requests
import schedule
import threading
import time
from datetime import datetime

#!\Users\alber\OneDrive\Documentos\Scripts
# -- coding: utf-8 --
# Configuración inicial
NESSUS_URL = "https://<TU_NESSUS_URL>"  # Reemplaza con la URL de tu instancia de Nessus
ACCESS_KEY = "<TU_ACCESS_KEY>"         # Reemplaza con tu Access Key
SECRET_KEY = "<TU_SECRET_KEY>"         # Reemplaza con tu Secret Key

HEADERS = {
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}",
    "Content-Type": "application/json"
}

def obtener_escaneos():
    #"""Obtiene la lista de escaneos desde Nessus."""
    url = f"{NESSUS_URL}/scans"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("scans", [])
    else:
        print(f"Error al obtener escaneos: {response.status_code} - {response.text}")
        return []

def pausar_escaneo(scan_id):
    #"""Pausa un escaneo activo."""
    url = f"{NESSUS_URL}/scans/{scan_id}/pause"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Escaneo {scan_id} pausado exitosamente.")
    else:
        print(f"Error al pausar escaneo {scan_id}: {response.status_code} - {response.text}")

def reanudar_escaneo(scan_id):
    #"""Reanuda un escaneo pausado."""
    url = f"{NESSUS_URL}/scans/{scan_id}/resume"
    response = requests.post(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"Escaneo {scan_id} reanudado exitosamente.")
    else:
        print(f"Error al reanudar escaneo {scan_id}: {response.status_code} - {response.text}")

def programar_pausa(scan_id, hora):
    #"""Programa la pausa de un escaneo a una hora específica."""
    schedule.every().day.at(hora).do(pausar_escaneo, scan_id=scan_id)
    print(f"Pausa programada para el escaneo {scan_id} a las {hora}.")

def programar_reanudacion(scan_id, hora):
    #"""Programa la reanudación de un escaneo a una hora específica."""
    schedule.every().day.at(hora).do(reanudar_escaneo, scan_id=scan_id)
    print(f"Reanudación programada para el escaneo {scan_id} a las {hora}.")

def ejecutar_schedule():
    #"""Ejecuta los trabajos programados en segundo plano."""
    while True:
        schedule.run_pending()
        time.sleep(1)

def mostrar_menu():
    #"""Muestra un menú para interactuar con los escaneos."""
    escaneos = obtener_escaneos()
    if not escaneos:
        print("No se encontraron escaneos.")
        return

    print("\nEscaneos disponibles:")
    for scan in escaneos:
        print(f"ID: {scan['id']} | Nombre: {scan['name']} | Estado: {scan['status']}")

    while True:
        print("\nOpciones:")
        print("1. Pausar un escaneo ahora")
        print("2. Reanudar un escaneo ahora")
        print("3. Programar pausa")
        print("4. Programar reanudación")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            scan_id = input("Ingresa el ID del escaneo a pausar: ")
            pausar_escaneo(scan_id)
        elif opcion == "2":
            scan_id = input("Ingresa el ID del escaneo a reanudar: ")
            reanudar_escaneo(scan_id)
        elif opcion == "3":
            scan_id = input("Ingresa el ID del escaneo a pausar: ")
            hora = input("Ingresa la hora para pausar (formato HH:MM): ")
            programar_pausa(scan_id, hora)
        elif opcion == "4":
            scan_id = input("Ingresa el ID del escaneo a reanudar: ")
            hora = input("Ingresa la hora para reanudar (formato HH:MM): ")
            programar_reanudacion(scan_id, hora)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

if __name__ == "__main__":
    # Ejecutar la planificación en un hilo separado
    threading.Thread(target=ejecutar_schedule, daemon=True).start()
    mostrar_menu()
