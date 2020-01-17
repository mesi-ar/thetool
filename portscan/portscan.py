#!/usr/bin/env python3

import socket, subprocess, sys, os, re
import sqlite3
from datetime import datetime
import geoip2.database

global ip1, ip2, por1, port2, loip1, loip2 #variaveis globais

#declaração de funções

def ipcheck(ip): #função de validação de ip baseada em expressões regulares
	regip = "(?:\b|^)((?:(?:(?:\d)|(?:\d{2})|(?:1\d{2})|(?:2[0-4]\d)|(?:25[0-5]))\.){3}(?:(?:(?:\d)|(?:\d{2})|(?:1\d{2})|(?:2[0-4]\d)|(?:25[0-5]))))(?:\b|$)"
	match = re.match(regip, ip)
	if match:
	    return True
	else:
	    return False

def portcheck(port): #função de validação de porto
	if port >= 1 and port <= 65535:
		return True	
	else:
		return False

def bd(dbName): #função de criação da base de dados
    dbIsNew = not os.path.exists(dbName)

    connbd=sqlite3.connect(dbName)

    if dbIsNew:
	    sql = """create table portscan (
	    id  integer primary key autoincrement not null,
	    ip  text,
	    openport    text,
	    srcip    text,
	    city 	text,
	    timestamp timestamp);"""

	    connbd.executescript(sql)
	    connbd.commit()
	    connbd.close()
	    print ("Base dados criado com sucesso\n")


if __name__ == '__main__':

	subprocess.call('clear',shell=True)

	print ("""\
                  _                       
                 | |                      
 _ __   ___  _ __| |_ ___  ___ __ _ _ __  
| '_ \ / _ \| '__| __/ __|/ __/ _` | '_ \ 
| |_) | (_) | |  | |_\__ \ (_| (_| | | | |
| .__/ \___/|_|   \__|___/\___\__,_|_| |_|
| |                                       
|_|                                                 

Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Portscan
	""")

	host = socket.gethostname()
	ip = socket.gethostbyname(host)
	print("Endereço IP[v4] local:", ip,"\n") #imprime endereço ip local

	#bd sqlite
	dbName = "./portscan/portscan.db"
	bd(dbName)

	#bd geoip
	bdgeoip = geoip2.database.Reader('../final/geoip/GeoLite2-City.mmdb') #variavel de inciação da base de dados GeoIP

	#ciclo de introdução e validação de ip inicial
	while True:
		ip1 = input("Introduz o IP inicial [IPv4]: ")
		if not ip1:
			print ("Esqueceste de introduzir o IP...!")
		elif ipcheck(ip1) == True:
			loip1 = ip1.split(".")
			loip1 = int(loip1[3]) #identificaçao de ultimo octeto do ip introduzido
			break
		else:
			print ("Erro na formatação do IP!")

	#ciclo de introdução e validação de ip final
	while True:
		ip2 = input("Introduz o IP final [Carrega em ENTER para ser o mesmo]: ")
		if not ip2:
			ip2 = ip1
			loip2 = loip1
			break
		elif ipcheck(ip2) == True:
			loip2 = ip2.split(".")
			loip2 = int(loip2[3])
			if loip2 < loip1:
				print ("O IP final tem de ser posterior ao IP inicial")
			else:
				break
		else:
			print ("Erro na formatação do IP!")


	#ciclo de introdução e validação de porto inicial
	while True:
		port1 = int(input("Introduz o porto inicial [1:65535]: "))
		if not port1:
			print ("Esqueceste de introduzir o porto...!")
		elif portcheck(port1) == True:
			break
		else:
			print ("Erro na porta especificada")

	#ciclo de introdução e validação de porto final
	while True:
		port2 = int(input("Introduz o porto final [1:62555][Carrega em ENTER para ser o mesmo]: "))
		if not port2:
			port2 = port1
			break
		elif port2 < port1:
			print ("O número introduzido tem de ser superior ao porto inicial")
		elif portcheck(port2) == True:
			break
		else:
			print ("Erro na porta especificada")


	t1 = datetime.now() #hora de inicio do processo

	iprange = ip1.split(".")#utilizado para definiar a gama de ips

	#ciclo de execução
	for x in range(loip1, (loip2 + 1)):

		curr_ip = iprange[0] + "." + iprange[1] + "." + iprange[2] + "." + str(x)
		print ("Endereço actual:-->", curr_ip)
		
		#valida de ip existe na bd geoip e retira a localização
		try:
			curr_ip_geo = bdgeoip.city(curr_ip)
			city = curr_ip_geo.city.names['en'] + ", " + curr_ip_geo.country.iso_code
		except:
			city = "ND"	#valor caso não exista na bd geoip
			pass
		print ("Localização:", city)
				
		for port in range(port1,port2):#ciclo de execução do portscan
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			socket.setdefaulttimeout(1)
			result = sock.connect_ex((curr_ip,port))
			if result == 0:
				print ("Porto aberto:-->\t", port)
				sock.close()
				connbd=sqlite3.connect(dbName)
				connbd.execute("insert into portscan(ip, openport, srcip, city, timestamp) values (?,?,?,?,?)", (str(curr_ip), str(port), str(ip), city, datetime.now())) 
				connbd.commit()
				connbd.close()
		
	#duraçao de scan
	t2 = datetime.now()
	total = t2-t1
	print ("O scan demorou " , total) 
