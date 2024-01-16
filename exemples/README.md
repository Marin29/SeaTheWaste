## Pour lancer le projet vous devez :

Réaliser les branchements des modules à la RPI:<br>
- Le module quectel BG96 se branche à un port USB de la RPI, on y inserre la carte SIM<br>
- Le module Draguino LA66 se branche à un port USB de la RPI<br>
- Le module Sigfox Breakout board BRKWS01 se branche aux pins de la RPI avec les branchements suivants : TX -> GPIO15(RX) / RX -> GPIO14(TX) / (+) -> 3V3 / (-) -> Ground

rentrer les commandes suivantes dans deux terminaux différents :<br>
`python3 app.py`<br>
`python3 mqtt.py`<br>
dans son téléphone ou son ordinateur connecter au même réseau que la RPI utiliser l'url suivant : http://192.168.192.98:5000/benchmark -> remplacer 192.168.192.98 par l'adresse correspondante à la RPI et à l'ordinateur/téléphone.<br>
Cette adresse risque de changer entre les diférentes connexion c'est pourquoi il est préférable de la fixer si jamais on utilise souvent le même réseau pour cela vous pouvez suivre le tutoriel suivant : [tuto pour fixer l'adresse de la RPI](https://raspberry-pi.fr/ip-locale-fixe/)<br><br>
Une fois sur le téléphone on choisit les réseaux à tester et la taille du message à envoyer. <br><br>
Lorsque l'on lance un test pour un réseau donné, si le réseau est disponible on est censé se connecter directement à ce dernier. Cependant dans le cas du LoRaWAN le processus de jointure peut prendre jusqu'à 1h30. Lancer le test permet de lancer le processus de jointure. Pour vérifier si le processus de jointure est bien en cours, on peut s'informer sur la plateforme the things network. La récurence si dessous montre que le processus est en cours :<br><br>
![image info](jointure_lorawan.png)<br><br>
Quand la jointure s'est faite on a différente façon de le voir :<br>
- Une led verte s'allume sur le module au moment de la jointure (pas en continu)<br>
- Un message JOINED s'affiche sur le moniteur série (pour accéder au port série on peut utiliser minicom avce un baudrate 9600)<br>
- Si l'on active verbose stream sur live data dans The Things network, il est possible de voir un retour <br>
- Enfin pour ne pas toucher au back on peut simplement essayer d'envoyer des messages pour voir si le message s'envoie<br>

## Bugs possibles et comment les résoudre :

Les ports USB utilisés par les composants peuvent changer au redémarage du boîtier.
La commande `ls /dev/tty*` permet d'afficher les ports utilisés. Le BG96 en prend 4 (USB1/2/3/4 en temps normal) et le LA66 1(USB0 en temps normal)
Pour résoudre le problème il suffit de modifier la `ligne 12 de test_nbiot.py`, `ligne 12 de test_ltem.py`, `ligne 6 de test_lora.py`

La migration vers Azure étant récente, elle n'est pas encore mature. Il peut donc arriver que certains bugs apparaissent.<br>
- il est parfois nécessaire  de relancer le partage de connexion pour résoudre le non envoi des données sur Azure

Il est possible de mettre en commentaire la lignes de ce type dans les fichiers `test_*.py`: <br>
![image info](ligne_de_code_azure.png)<br><br>

## Plateformes qui rentrent en jeu dans le test :

Azure et Cumulocity sont dans le cas où tout fonctionne les seules plateformes à consulter, cependant il est important d'avoir connaissance des autres plateformes dans la résolution de quelques bugs.

- [The Things Network](https://eu1.cloud.thethings.network/console/) : cette plateforme permet d'avoir accés à un réseau LoRaWAN collaboratif, qui est utilisé pour le test.

- [Backend Sigfox](https://backend.sigfox.com/) : cette plateforme permet de gérer les paquets de données envoyées au réseau Sigfox.

- [Broker MQTT Adafruit](https://io.adafruit.com/mtulard/feeds/lora) : plateforme sur laquelle le message test est envoyé pour les réseaux NB-IoT et LTE-M.