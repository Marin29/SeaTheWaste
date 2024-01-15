import serial
import pynmea2
from time import sleep
def GPS():
    # Configuration du port série pour la communication avec le module BG96
    port = '/dev/ttyUSB4'  # Remplacez par le bon port série si nécessaire
    baudrate = 115200
    
    # Configuration du port série pour la communication avec le module BG96
    ser = serial.Serial(port, baudrate)

    # Commande pour activer le mode GPS
    ser.write(b'ATI\r\n')
    sleep(10)
    line = ser.readline().strip()
    print(line)

    # Lecture des données GPS
    while False:
        # Lecture de la ligne du port série
        line = ser.read(2).strip()
    
        # Vérification si la ligne contient les données GPS
        if line.startswith('$GNGGA'):
            try:
                # Analyse des données NMEA
                msg = pynmea2.parse(line)
            
                # Récupération de la latitude et de la longitude
                latitude = msg.latitude
                longitude = msg.longitude
            
                # Affichage des coordonnées GPS
                print(f'Latitude: {latitude:.6f}')
                print(f'Longitude: {longitude:.6f}')
            
                # Sortie de la boucle après avoir obtenu les coordonnées GPS
                break
            except pynmea2.ParseError:
                continue

    # Commande pour désactiver le mode GPS
    ser.write(b'AT+QGPSEND\r\n')

    # Fermeture du port série
    ser.close()
    
GPS()    
    

