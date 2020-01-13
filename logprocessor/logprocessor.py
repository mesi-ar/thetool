#!/usr/bin/python3

"""
TODO
1. ver se ha auth.log com mais serviços
2. criar mais paginas no pdf
3. implementar tab completation no path

"""

import socket, subprocess, sys, os
import sqlite3
from datetime import datetime
import geoip2.database
import re
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape

#log para bd
def log2bd(log):
	f = open(log, "r")
	lines = f.readlines()
	print ("A processar log...")
	for line in lines:
		words = line.split()
		ip = str(re.findall(r"(?:\b|^)((?:(?:(?:\d)|(?:\d{2})|(?:1\d{2})|(?:2[0-4]\d)|(?:25[0-5]))\.){3}(?:(?:(?:\d)|(?:\d{2})|(?:1\d{2})|(?:2[0-4]\d)|(?:25[0-5]))))(?:\b|$)",str(words[4:])))
		
		#remove bad chars
		bad_chars = ["['","']","[]"]
		for i in bad_chars : 
			ip = ip.replace(i, '')
			if ip == "":
				ip = "ND"

		try:
			ip_geo = bdgeoip.city(ip)
			city = ip_geo.city.names['en'] + ", " + ip_geo.country.iso_code
		except:
			city = "ND"
			pass

		connbd=sqlite3.connect(dbName)
		connbd.execute("insert into logprocessor(month, day, time, hostname, service, msg, ip, city) values (?,?,?,?,?,?,?,?)", (words[0],words[1],words[2],words[3],words[4], str(words[5:]), str(ip), city)) 
		connbd.commit()
		connbd.close()

def report(dbName):

	#bd
	connbd = sqlite3.connect(dbName)
	connbd.row_factory = sqlite3.Row
	cur = connbd.cursor()
	cur.execute("SELECT month, day, time, hostname, service, ip, city FROM logprocessor WHERE (service like 'ssh%' OR service like 'http%') AND city != 'ND'")
	rows = cur.fetchall()

	#pdf
	pdf = "./logprocessor/logprocessor.pdf"
	canvas_obj = canvas.Canvas(pdf,
	                           pagesize=(landscape(letter)))

	# Create textobject
	textobject = canvas_obj.beginText()

	# Set text location (x, y)
	textobject.setTextOrigin(20, 580)

	textobject.setFillColor(colors.red)
	textobject.textLine(text="##### REPORT LOGPROCESSOR #####")

	textobject.setFillColor(colors.black)
	for row in rows:
		line = str(dict(row))
		textobject.textLine(line)

	canvas_obj.drawText(textobject)
	canvas_obj.save()

	os.popen('evince ' + pdf)

def bd(dbName):
	os.remove(dbName)

	connbd=sqlite3.connect(dbName)

	sql = """create table logprocessor (
	id  integer primary key autoincrement not null,
	month	text,
	day		text,
	time 	text,
	hostname	text,
	service	text,
	msg		text,
	ip  	text,
	city	text);"""
	connbd.executescript(sql)
	connbd.commit()
	connbd.close()

if __name__ == '__main__':	

	subprocess.call('clear',shell=True)

	print ("""\
 _                                                          
| |                                                         
| | ___   __ _ _ __  _ __ ___   ___ ___  ___ ___  ___  _ __ 
| |/ _ \ / _` | '_ \| '__/ _ \ / __/ _ \/ __/ __|/ _ \| '__|
| | (_) | (_| | |_) | | | (_) | (_|  __/\__ \__ \ (_) | |   
|_|\___/ \__, | .__/|_|  \___/ \___\___||___/___/\___/|_|   
          __/ | |                                           
         |___/|_|                                           

Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: LogProcessor [auth.log]
	""")

	#bd sqlite
	dbName = "./logprocessor/logprocessor.db"

	bd(dbName)

	#bd geoip
	bdgeoip = geoip2.database.Reader('../final/geoip/GeoLite2-City.mmdb')

	log = input("Qual é o caminho para o log [auth.log]?\n")
	log = "/media/r2d2/data/mestrado/ano2/lpd/trabalho/final/logprocessor/logs/auth.log"
	log2bd(log)
	r = input("Queres o relatorio em pdf?\n")
	if r in ["s","S","SIM","Sim","sim"]:
		report(dbName)

