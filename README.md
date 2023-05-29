# Multithreaded File Transfer using TCP Socket in Python
# Proiect_Retele_Gr1090_Stancu-Gheorghe-Mirel_Radulescu-Denis-Andrei_Rusu-Robert

A multithreaded file transfer client-server program build using a python programming language. The server has the capability to handle multiple clients concurrently at the same by using threading. The server assigns each client a thread to handle working for that client. 

The server supports the following functions:
 - LISTSERVER: List all the files from the server.
 - LISTCLIENT: List all the files from the clients.
 - LISTDOWNLOAD: List all the files downloaded.
 - UPLOAD path: Upload a file to the server
 - DELETE filename: Delete a file from the server
 - LOGOUT: Disconnect from the server
 - HELP: List all the commands


Partajarea fisierelor:
Clientul se autentifica prin cont, trimitand server-ului o lista cu fisierele pe care le publica, si primeste lista tuturor fisierelor publicate de catre ceilalti clienti autentificati; da
Cand un client se autentifica, ceilalti clienti autentificati primesc o notificare de adaugare a acesuia, impreuna cu lista de fisiere pe care o publica; da
Cand un client isi incheie sesiunea cu server-ul, aceste ii confirma incheierea sesiunii si notifica ceilalti clienti autentificati sa stearga din lista clientul respectiv; da
Un client poate solocita server-ului descarcarea unui fisier de la alti clienti;
Server-ul solicita detinatorului fisierului respetiv citirea continutului acestuia;
Ulterior, server-ul livreaza continutul fisierului clientului care l-a solicitat;
Clientul salveaza fisierul in sistemul sau de fisiere;
Fiecare client va avea un director gazda expus, care va fi monitorizat;
La adaugarea unui nou fisier in acest director, clientul va notifica prin intermediul server-ului adaugarea fisierului;
La stergerea unui fisier din acest director, clientul va notifica in mod similar ceilalti clienti prin intermediul server-ului.

 
