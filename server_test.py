from threading import Thread
import socket
import sys
import os
import time

fin = True

def receive(client):
    
    requete = client.recv(500)
    requete = requete.decode('utf-8')
    print(requete)
    if not requete :
        print('close')
        

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
        time.sleep(5)
        sys.exit()



clientSocket.close()
s.close()