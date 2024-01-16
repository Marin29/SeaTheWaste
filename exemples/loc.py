from time import sleep
import serial

def parse_gps_data(gps_data):
    #match = re.search(r'\+CGNSINF: \d,\d,(\d{14}\.\d+),([\d.]+),([\d.]+)', gps_data)
   
    s = gps_data.split(',')

    dat = s[2]
    lat = s[3]
    lon = s[4]
    return dat, lat, lon

def localisation():
    # Connexion au port série (à adapter en fonction de votre configuration)
    #ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

    # Configuration du port série pour la communication avec le module BG96
    port = '/dev/ttyUSB0'  # Remplacez par le bon port série si nécessaire
    baudrate = 115200
   
    ser = serial.Serial(port, baudrate, timeout=1)

    # Verification Connection
    ser.write(b'AT\r\n')
    sleep(1)
    lin = ser.readline().strip()
    line = ser.readline().strip()
    print(line)

    # Power On
    ser.write(b'AT+CGNSPWR=1 \r\n')
    sleep(5)
    lin = ser.readline().strip()
    line = ser.readline().strip()
    print(line)

    # Information Date, Latitude, Longitude
    ser.write(b'AT+CGNSINF\r\n')
    sleep(2)
    lin = ser.readline().strip()
    line = ser.readline().strip()
    print(line)

    # Fermeture du port série
    ser.close()

    # Affichage des données séparées
    parsed_data = parse_gps_data(line)

    if parsed_data:
        timestamp, latitude, longitude = parsed_data
        print(f"Date: {timestamp}, Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Les données GPS n'ont pas pu être extraites.")
    
    return parsed_data