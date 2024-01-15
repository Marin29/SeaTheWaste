from time import sleep #permet de marquer des temps de pauses 
import serial #bibliothèque permettant de'utiliser un moniteur série afin de communiquer avec les ports série 
import time #bibliothèque utile pour calculer le temps d'envoie du message 


ser=serial.Serial("/dev/ttyUSB0") #on définit le port série utilisé 
ser.baudrate=9600 #vitesse de transmission sur le port série

        
def AT(commande,dodo):#fonction qui permet d'envoyer des commandes AT
    ser.reset_input_buffer() #on nétoie le moniteur série
    print("on lance une nouvelle commande AT",commande)#permet de vérifier dans la console que la commande AT s'envoie bien
    EnvoyerEnOctet("AT+"+commande+"\r\n")#syntaxe de base propre à l'ensemble des commandes AT du module LA66
    sleep(dodo)#on prend un temps de pause pour anticiper le temps pris avant la réception d'une réponse à la commande AT 
    data=ser.read_all()#on lie la ligne renvoyée sur le moniteur série
    data=data.strip()
    print(data)#permet d'afficher ce qu'on a lu dans la console
    
    return data#on renvoie la valeur qui a été retourné par le module et lu sur le moniteur série

def EnvoyerEnOctet(commande):#fonction qui permet la conversion en octet, pour que le module comprenne les commandes AT envoyées
    ser.write(commande.encode())

#Fonctions permettant l'envoi des commandes AT nécessaires à la récupération des données composant le diagnostic
#informations utilent à l'idnetification OTAA
def LoraInfo1():
    info= AT("APPKEY=?",0.5)
    return info
def LoraInfo2():
    info=AT("APPEUI=?",0.5)
    #AT("APPEUI=A224100000000101",0.5)
    return info
def LoraInfo3():
    #AT("DEUI=A2241015645784B4",0.5)
    info=AT("DEUI=?",0.1)
    return info
#puissance de transfert
def LoraInfo4():
    info= AT("TXP=?",0.5)
    return info
#on vérifie la connexion
def LoraInfo6():
    info= AT("NJS=?",0.5)
    return info
def LoraInfo7():
    info= AT("DR=?",0.5)
    return info


def LoraSend(x):
    send="null"
    connection=LoraInfo6()
    if connection==b'0\r\n\r\nOK':
        AT("JOIN",2)
        send=b''
    else:
        x=str(x)+str(x)
        taille=int(len(x))/2
        taille=int(taille)
        send=AT("SENDB=01,02,"+str(taille)+","+x,5)
    return send

def test(x):#fonction qui permet de tester le réseau LoraWAN, en y envoyant un message x d'un nombre choisi d'octet
#     d1=LoraInfo1() #APPKEY
#     d2=LoraInfo2() #APPEUI
    d3=LoraInfo3() #DEUI
#     d4=LoraInfo4() #TXP
#     d6=LoraInfo6() #NJS
    d7=LoraInfo7() #DR

    
    if ser.isOpen:#on vérifie que le port est bien ouvert
        print("le port est bien ouvert")
        send=LoraSend(x)
        #définition d'un bouléen permettant de s'assurer du bonne envoie du message au réseau
        if b'OK' in send:
            sendconf=True
        else:
            sendconf=False
        return sendconf    
       

#On récupère les infos du diagnostics pour pouvoir les réutiliser dans les autres programmes
def get_AT1():
    d=LoraInfo1()
    return d
def get_AT2():
    d=LoraInfo2()
    return d
def get_AT3():
    d=LoraInfo3()
    return d
def get_AT4():
    d=LoraInfo4()
    return d
def get_AT5():
    d=LoraInfo5()
    return d
def get_AT7():
    d=LoraInfo7()
    return d


#test("a")
