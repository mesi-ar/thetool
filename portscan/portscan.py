#!/usr/bin/env python
# -*- coding: utf-8 -*-

 

'''
TODO
.validar ip e porta quando passados nos argumentos
.trabalhar nos timeouts e nos erros
.usar variavel global para rmip
usar classes
'''

import socket, subprocess, sys
from datetime import datetime
from termcolor import colored, cprint

subprocess.call('clear',shell=True)

cprint ("""\
 __  __ _____ ____ ___      _  ___  _  ___  
|  \/  | ____/ ___|_ _|    / |( _ )/ |/ _ \ 
| |\/| |  _| \___ \| |_____| |/ _ \| | (_) |
| |  | | |___ ___) | |_____| | (_) | |\__, |
|_|  |_|_____|____/___|    |_|\___/|_|  /_/@IPBeja
""","blue")

cprint ("""\
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Scanner de Portos de Rede
""","green")


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
	rmip1 = raw_input("Introduza o IP inicial [IPv4]: ")

	if not rmip1:
		cprint ("Esqueceu-se de introduzir o IP inicial...!","red")
		return True
	elif valida_ip(rmip1) == False:
		cprint ("Erro na formatação do IP!","red")
		return True
	else:
		return False

def val_rmip2(): #função para validar remote ip2

	global rmip2
	rmip2 = raw_input("Introduza o IP final [Carregue em ENTER para ser o mesmo]: ")

	if not rmip2:
		return False
	elif valida_ip(rmip2) == False:
		cprint ("Erro na formatação do IP!","red")
		return True
	else:
		return False

def val_rmport1(): #funçao para validacao de porta inicial

	global rmport1
	rmport1 = int(raw_input("Insira o porto inicial: "))

	if not rmport1:
		cprint ("Esqueceu-se de introduzir o porto inicial...!","red")
		return True
	elif rmport1 < 1 and rmport1 > 65555:
		cprint ("Erro na porta especificada","red")
		return True
	else:
		return False

def val_rmport2(): #funçao para validacao de porta final

	global rmport1, rmport2
	rmport2q = raw_input("Introduza o porto final [Carregue em ENTER para ser o mesmo]: ")

	if not rmport2q:
		rmport2 = rmport1 + 1
		return False
	elif rmport2q <= 1 and rmport2q >= 65555:
		cprint ("Erro na porta especificada","red")
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
	print "Endereço actual:-->", curr_ip
		
	for port in range(rmport1,rmport2):
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result = sock.connect_ex((curr_ip,port))
		if result == 0:
			print "Porto aberto:-->\t", port
			sock.close()
	
#duraçao de scan
t2 = datetime.now()
total = t2-t1
print "O scan demorou " , total 
