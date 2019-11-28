#!/usr/bin/env python3

'''
TODO
1. passar para python3 (ver erros) #FEITO
2. validar ip e porta quando passados nos argumentos
3.trabalhar nos timeouts e nos erros
4. usar variavel global para rmip
5. geoip #FEITO
6. usar __main__
'''

import socket, subprocess, sys, os
import sqlite3
from datetime import datetime
import geoip2.database

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

Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Portscan
""")

host = socket.gethostname()
ip = socket.gethostbyname(host)
print("Endereço IP[v4] local:", ip,"\n")

#bd sqlite
dbName = "./portscan/portscan.db"
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

#bd geoip
bdgeoip = geoip2.database.Reader('../final/geoip/GeoLite2-City.mmdb')

#declaração de funções
def valida_ip(ip): #função para validar endereço ipv4
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

def val_rmip1(): #função para validar remote ip1

	global rmip1
	rmip1 = input("Introduza o IP inicial [IPv4]: ")

	if not rmip1:
		print ("Esqueceu-se de introduzir o IP inicial...!")
		return True
	elif valida_ip(rmip1) == False:
		print ("Erro na formatação do IP!")
		return True
	else:
		return False

def val_rmip2(): #função para validar remote ip2

	global rmip2
	rmip2 = input("Introduza o IP final [Carregue em ENTER para ser o mesmo]: ")

	if not rmip2:
		return False
	elif valida_ip(rmip2) == False:
		print ("Erro na formatação do IP!")
		return True
	else:
		return False

def val_rmport1(): #funçao para validacao de porta inicial

	global rmport1
	rmport1 = int(input("Insira o porto inicial: "))

	if not rmport1:
		print ("Esqueceu-se de introduzir o porto inicial...!")
		return True
	elif rmport1 < 1 and rmport1 > 65555:
		print ("Erro na porta especificada")
		return True
	else:
		return False

def val_rmport2(): #funçao para validacao de porta final

	global rmport1, rmport2
	rmport2q = input("Introduza o porto final [Carregue em ENTER para ser o mesmo]: ")

	if not rmport2q:
		rmport2 = rmport1 + 1
		return False
	elif int(rmport2q) <= 1 and int(rmport2q) >= 65555:
		print ("Erro na porta especificada")
		return True
	else:
		rmport2 = int(rmport2q)
		return False

#recebe ips e portas como argumento
if len(sys.argv) > 1: 
	rmip1 = sys.argv[1]
	if sys.argv[2] is not None:
		rmip2 = sys.argv[2]
	else:
		rmip2 = ""
	rmport1 = int(sys.argv[3])
	if sys.argv[4] is not None:
		rmport2 = int(sys.argv[4])
	else:
		rmport2 = 0
else:
	rmip1 = ""
	rmip2 = ""
	rmport1 = 0
	rmport2 = 0

#introdução de ips
	while val_rmip1():
		pass 

	while val_rmip2():
		pass 

	#introdução de portas
	while val_rmport1():
		pass 

	while val_rmport2():
		pass 

#obtençao de ultimo octeto dos ips para utilização no ciclo de scan
ip1 = rmip1.split(".") 
loip1 = int(ip1[3])

if not rmip2:
	loip2 = loip1
else:
	ip2 = rmip2.split(".") 
	loip2 = int(ip2[3])

t1 = datetime.now() #hora de inicio

#scan
for x in range(loip1, (loip2 + 1)):

	curr_ip = ip1[0] + "." + ip1[1] + "." + ip1[2] + "." + str(x)
	print ("Endereço actual:-->", curr_ip)
	
	#valida de ip existe na bd geoip
	try:
		curr_ip_geo = bdgeoip.city(curr_ip)
		city = curr_ip_geo.city.names['en'] + ", " + curr_ip_geo.country.iso_code
	except:
		city = "ND"	
		pass
	print ("Localização:", city)
			
	for port in range(rmport1,rmport2):
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
