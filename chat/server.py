#!/usr/bin/env python3

import socket, subprocess, sys, os
from cryptography.fernet import Fernet
import sqlite3
from datetime import datetime

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

print ("""\
##### S E R V E R ######\n
Inicia o programa client.py para iniciar a comunicação
""")

#criação da base de dados
dbName = "./chat/chat.db"
dbIsNew = not os.path.exists(dbName)

connbd=sqlite3.connect(dbName)
if dbIsNew:
    sql = """create table chat (
    id  integer primary key autoincrement not null,
    ip  text,
    name    text,
    type    text,
    msg     text,
    cipherkey    text,
    timestamp timestamp);"""
    connbd.executescript(sql)
    connbd.commit()
    connbd.close()
    print ("Base dados criado com sucesso\n")

#criacao da chave de encriptacao
key = Fernet.generate_key()
cipher = Fernet(key)
print ("A chave de encriptação a enviar é", key.decode(), "\n")

s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print("IP do servidor para transmitir ao cliente", ip,"\n")

name = input("Como te chamas? ")
           
s.listen(1)
print("\nEsperando cliente...\n")

conn, addr = s.accept()
print("Cliente ligado ", addr[0], "(", addr[1], ")\n")

#envia chave de encriptação
conn.send(bytes(key))

#recebe nome do cliente
c_name = conn.recv(1024) 
c_name = c_name.decode() 
print(c_name, "ligou-se com usando o socket", addr[0], ":", addr[1],". \nEscreve hasta para sair do chat.\n")

#envia nome do servidor
nameclr = name.encode()
name = cipher.encrypt(nameclr)
conn.send(name) 

#ciclo de conversação
while True:
    message = input(str("Eu: "))
    if message == "hasta":
        message = "Saiu do chat!"
        message = message.encode()
        message = cipher.encrypt(message)
        conn.send(message) 
        conn.close()
        break
    #envia mensagem para cliente
    message = message.encode()
    message = cipher.encrypt(message)
    conn.send(message)
    connbd=sqlite3.connect(dbName)
    connbd.execute("insert into chat(ip, name,type,msg,cipherkey,timestamp) values (?,?,?,?,?,?)", (ip,nameclr,"server", message, key.decode(), datetime.now())) 
    connbd.commit()
    connbd.close()
    #recebe mensagem do cliente
    ciphermessage = conn.recv(1024) 
    message = cipher.decrypt(ciphermessage)
    message = message.decode() 
    print(c_name, ":", message)
    connbd=sqlite3.connect(dbName)
    connbd.execute("insert into chat(ip, name,type,msg,cipherkey,timestamp) values (?,?,?,?,?,?)", (addr[0],c_name,"client", ciphermessage, key.decode(), datetime.now())) 
    connbd.commit()
    connbd.close()
