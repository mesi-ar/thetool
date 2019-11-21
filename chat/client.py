#!/usr/bin/env python3

from socket import *
from threading import Thread
from cryptography.fernet import Fernet #

def receive():
    
    key = client_socket.recv(BUFSIZ) #recebe a chave do servidor
    global cipher #variavel global para definicao da cifra
    cipher = Fernet(key) #cifra
    print ("A chave de encriptação recebida do servidor é", key.decode())
    
    while True:
        ciphermsg = client_socket.recv(BUFSIZ).decode()
        s = ciphermsg.split(":")
        #msg = cipher.decrypt(ciphermsg)
        #msg = msg.decode()
        #print (msg)
        #print (s[1]) #FIQUEI AQUI!! da erro ao desencriptar porque o nome nao vai encruptador. tentar seprar o nome ou encripta-lo tambem
        print (ciphermsg)
        #msg = msg.decode()
        """if msg == "{quit}":
            client_socket.close()
            break
        if not msg:
            break
        print(msg)"""


def send():
    while True:
        msg = input()
        msg = msg.encode()
        #print (cipher)
        ciphermsg = cipher.encrypt(msg)
        client_socket.send(ciphermsg)
        #client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            break


HOST = "127.0.0.1"#input('Enter host: ')
PORT = 33000#input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()