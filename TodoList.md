## En cours : 

 - Options -l et -k à implémenter
 - Envoyer des requêtes depuis vers le serveur vers le client pour remettre à 0 le timer, supprimer le fichier, etc..

## Problèmes?

 - L'option -k doit kill le processus, mais depuis un autre cmd?? car l'option ne peut pas être lancé avec le programme, donc il faut que le programme tourne en fond et il faut récup l'id du processus pour le kill, mais il faudra faire très attention
 - L'arrêt du serveur via except --> KeyboardInterrupt ne marche pas actuellement (voir dessus des options alternatives pour arreter le serv/client https://python.doctor/page-reseaux-sockets-python-port)
 - Il faut que en arrêtant le serveur cela ping le client pour lui dire de s'arreter et de supprimer le fichier, dans le cas du except --> KeyboardInterrupt, regarder si d'abord le serveur s'arrete puis print le message ou l'inverse (on veut l'inverse). Il faudrait dans ce cas faire une except via une combinaison de touche autre que keyboard interrupt, dans l'exception faire la requete vers le client pour lui dire de s'arreter/supprimer le log, puis faire un socket.close ou qqchose de similaire.