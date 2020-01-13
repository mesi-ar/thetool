#!/usr/bin/env python3

import socket, subprocess, sys, os
from cryptography.fernet import Fernet

subprocess.call('clear',shell=True)

print ("""\
      _           _   
     | |         | |  
  ___| |__   __ _| |_ 
 / __| '_ \ / _` | __|
| (__| | | | (_| | |_ 
 \___|_| |_|\__,_|\__|                                               

Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Chat encriptado
""")

print ("##### C L I E N T ######\n")

s = socket.socket()
#shost = socket.gethostname()
#ip = socket.gethostbyname(shost)
host = input(str("Endereço do servidor: "))
#host = "172.16.10.20"
name = input(str("\nComo te chamas? "))
port = 1234

print("\nA ligar ao servidor ", host, "(", port, ")\n")

s.connect((host, port))
print("Sucesso...\n")

#recebe a chave do servidor
key = s.recv(1024) 
cipher = Fernet(key) #cifra
print ("A chave de encriptação recebida do servidor é", key.decode())

#envia nome do parceiro
s.send(name.encode())

#recebe nome do servidor 
s_name = s.recv(1024)
s_name = cipher.decrypt(s_name)
s_name = s_name.decode() 
print("\nSessão estabelecida com", s_name, ". \nEscreve hasta para sair do chat.\n")

while True:
    #recebe mensagem do servidor
    message = s.recv(1024) 
    message = cipher.decrypt(message)
    message = message.decode()
    print(s_name, ":", message)
    message = input(str("Eu: "))
    if message == "hasta":
        message = "Saiu do chat!"
        message = message.encode()
        message = cipher.encrypt(message)
        s.send(message) 
        s.close()
        break
    #envia mensagem para o servidor
    message = message.encode()
    message = cipher.encrypt(message)
    s.send(message) 
