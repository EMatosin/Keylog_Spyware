import socket
import os

def receive_file(filename, client_socket, destination_folder):
    full_path = os.path.join(destination_folder, filename)
    with open(full_path, 'wb') as file:
        while True:
            keylog = client_socket.recv(1024)
            if not keylog  :
                break
            file.write(keylog)

def main():
    server_address = '0.0.0.0'  # Adresse IP du serveur
    server_port = 6060  # Port du serveur
    destination_folder = "fichiers_recus"  # Répertoire de destination des fichiers reçus

    # Création du répertoire de destination s'il n'existe pas
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Création d'un socket serveur
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Liaison du socket à l'adresse et au port souhaités
        server_socket.bind((server_address, server_port))

        # Écoute des connexions entrantes
        server_socket.listen(5)
        print("Le serveur est prêt à écouter les connexions entrantes.")

        try:
            while True:
                # Attente d'une connexion entrante
                client_socket, client_address = server_socket.accept()
                print("Nouvelle connexion entrante:", client_address)

                # Réception du fichier envoyé par le client
                filename = "fichier_recu.txt"  # Nom du fichier reçu
                receive_file(filename, client_socket, destination_folder)

                print("Fichier reçu et enregistré avec succès:", filename)

        except KeyboardInterrupt:
            print("Arrêt du serveur.")

if __name__ == "__main__":
    main()