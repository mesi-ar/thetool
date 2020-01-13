#!/usr/bin/python3

import sys, subprocess, os

subprocess.call('clear',shell=True)

print ("""\
 _   _          _              _ 
| | | |        | |            | |
| |_| |__   ___| |_ ___   ___ | |
| __| '_ \ / _ \ __/ _ \ / _ \| |
| |_| | | |  __/ || (_) | (_) | |
 \__|_| |_|\___|\__\___/ \___/|_|                                              

Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
""")

if len(sys.argv) != 2:
	print ("""\
Utilização: python3 thetool.py [tool_a_executar]

[tool_a_executar]:
	portscan = efectua um varrimento aos portos abertos num segmento de rede e guarda em bdls 
	conn = verifica as ligações activas nesta maquina, guarda-as em bd e permite gerar graficos de ocurrencias
	chat = cria uma sala de conversação encriptada entre 2 elementos e guarda em
	logprocessor = processa ficheiro auth.log e gera relatorios pdf
	report = cria relatorios em pdf da utilização das tools chat e portscan
	""")
	sys.exit()	

#print ("Argumento", str(sys.argv[1]))
tool = str(sys.argv[1])

if tool == "portscan":
	os.system('python3 ./portscan/portscan.py')
elif tool == "conn":
	os.system('python3 ./conn/conn.py')
elif tool == "chat":
	os.system('python3 ./chat/server.py')
elif tool == "report":
	os.system('python3 ./report/report.py')
elif tool == "logprocessor":
	os.system('python3 ./logprocessor/logprocessor.py')
else:
	print ("Tool não implementada")
