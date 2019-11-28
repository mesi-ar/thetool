#!/usr/bin/python3

import os
import sqlite3

dbName = "chat.db"

#Verifica se base de dados existe
dbIsNew = not os.path.exists(dbName)

#Ligacao/Criacao da base de dados
conn=sqlite3.connect(dbName)
if dbIsNew:
	print ("Base dados criado com sucesso")
else:
	print ("Base dados ja existente")

sql = """create table chat (
	id	integer primary key autoincrement not null,
	ip 	text,
	name 	text,
	type	text,
	msg		text,
	timestamp timestamp);"""

#Executa o código SQL e cria a tabela sniff
conn.executescript(sql)
conn.commit()
conn.close()