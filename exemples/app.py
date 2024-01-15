from flask import Flask, request#cette bibliothèque permet la création d'une application web python
import position_gps
import lora_envoi


app = Flask(__name__)#on créer l'application Flask

@app.route('/benchmark', methods=['GET', 'POST'])
def form_example():
    write=""
    #au chargement de la page chaque variable est à 0 elles seront modifier grâce au formiulaire présent dans le return
    lorawan = request.form.get('lorawan',0)
    sigfox = request.form.get('sigfox',0)
    ltem = request.form.get('ltem',0)
    nbiot = request.form.get('nbiot',0)
    taille_message = request.form.get('taille_message',0)
    sub = request.form.get('sub',0)

    envoi=[False,False,False,False]
    
    #on définit chaque situation pour les faire correspondre à une condition de test_reseau
    if lorawan=="1" and sigfox==0 and ltem==0 and nbiot==0 :
        reseau=1
        write="LoRaWAN"
    elif lorawan==0 and sigfox=="1" and ltem==0 and nbiot==0 :
        reseau=2
        write="Sigfox"
    elif lorawan==0 and sigfox==0 and ltem==0 and nbiot=="1" :
        reseau=3
        write="NB-IoT"
    elif lorawan==0 and sigfox==0 and ltem=="1" and nbiot==0 :
        reseau=4
        write="LTE-M"
    elif lorawan=="1" and sigfox=="1" and ltem==0 and nbiot==0 :
        reseau=5
        write="LoRaWAN et Sigfox"
    elif lorawan==0 and sigfox==0 and ltem=="1" and nbiot=="1" :
        reseau=6
        write="NB-IoT et LTE-M"
    elif lorawan=="1" and sigfox==0 and ltem==0 and nbiot=="1" :
        reseau=7
        write="NB-IoT et LoRaWAN"
    elif lorawan=="1" and sigfox==0 and ltem=="1" and nbiot==0 :
        reseau=8
        write="LoRaWAN et LTE-M"
    elif lorawan==0 and sigfox=="1" and ltem=="1" and nbiot==0 :
        reseau=9
        write="Sigfox et LTE-M"
    elif lorawan==0 and sigfox=="1" and ltem==0 and nbiot=="1" :
        reseau=10
        write="NB-IoT et Sigfox"
    elif lorawan==0 and sigfox=="1" and ltem=="1" and nbiot=="1" :
        reseau=11
        write="Sigfox, NB-IoT et LTE-M "
    elif lorawan=="1" and sigfox==0 and ltem=="1" and nbiot=="1" :
        reseau=12
        write="LoRaWAN, NB-IoT et LTE-M"
    elif lorawan=="1" and sigfox=="1" and ltem=="1" and nbiot==0 :
        reseau=13
        write="LoRaWAN, Sigfox et LTE-M"
    elif lorawan=="1" and sigfox=="1" and ltem==0 and nbiot=="1" :
        reseau=14
        write="LoRaWAN, Sigfox et NB-IoT"
    elif lorawan=="1" and sigfox=="1" and ltem=="1" and nbiot=="1" :
        reseau=15
        write="LoRaWAN, Sigfox, NB-IoT et LTE-M"    
    elif lorawan==0 and sigfox==0 and ltem==0 and nbiot==0 :
        reseau=16
    else :
        reseau=17
        write=""
    if sub=="Submit" or reseau is None:    
        envoi=test_reseau.benchmark(int(taille_message),reseau) #lorsque le formulaire est envoyé on lance le test_reseau
        print(envoi) 
  
  #dans le return on code la page html/css avec avec laquelle on va pouvoir contrôler le test
    return '''
    <div style="background-color: f2f2f2; padding:50px; font : Arial, sans-serif;">
    <form method="POST" "max-width: 400px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);" >
    <h2 style="color: #333333; margin-top: 0;">Taille du message à envoyer (en octets) :</h2>
    <input type="number" name="taille_message" required style="margin-bottom: 10px;">
    
    <h2 styke="color: #333333; margin-top: 0;">Réseau sur lequel envoyer le message :</h2>
    <div>
        <input type="radio" id="lora" name="lorawan" value="1" style="margin-bottom: 10px;">
        <label for="lora" style:"margin-left: 5px;">LoRaWAN</label>
    </div>
    <div>
        <input type="radio" id="sigfox" name="sigfox" value="1" style="margin-bottom: 10px;">
        <label for="sigfox">Sigfox</label>
    </div>
    <div>
        <input type="radio" id="ltem" name="ltem" value="1" style="margin-bottom: 10px;">
        <label for="ltem">LTE-M</label>
    </div>
    <div>
        <input type="radio" id="nbiot" name="nbiot" value="1" style="margin-bottom: 10px;">
        <label for="nbiot">NB-IoT</label>
    </div>
    
    <br>
    <input type="submit" name="sub" value="Submit" style="background-color: #4CAF50; color: #ffffff; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
    <br>
    <br>
    </form>

    <h2 style="color: #333333; margin-top: 0;">Un message de {} octets va être envoyé au(x) réseau(x) suivant(s) : {}</h2>
    <br>
    <div>
    message envoyé à LoRaWAN : {}
    <br>
    message envoyé à Sigfox : {}
     <br>
    message envoyé à NB-IoT : {}
     <br>
    message envoyé à LTE-M : {}
    
    </div>'''.format(taille_message, write,envoi[0],envoi[1],envoi[2],envoi[3])#variables qui prnedront la place dabs les {}


if __name__=='__main__':
    app.run(host='172.20.10.3', debug=True, port=5000)#le host est à changer en cas de changement de réseau, il faut aussi penser à fixer l'adresse dans le cas d'un réseau qui risque d'être récurent(pour cela il faut suivre le tuto dans readme)
