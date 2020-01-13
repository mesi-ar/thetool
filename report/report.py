#!/usr/bin/python3

import sqlite3, subprocess
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os

def report(bd):

	#bd
	dbName = "./" + bd + "/" + bd + ".db"
	conn = sqlite3.connect(dbName)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM " + bd)
	rows = cur.fetchall()

	#pdf
	pdf = "./report/report_" + bd + ".pdf"
	canvas_obj = canvas.Canvas(pdf,
	                           pagesize=(1800,800))

	# Create textobject
	textobject = canvas_obj.beginText()

	# Set text location (x, y)
	textobject.setTextOrigin(20, 750)

	textobject.setFillColor(colors.red)
	textobject.textLine(text="##### REPORT " + bd.upper() + " #####")

	textobject.setFillColor(colors.black)
	for row in rows:
		line = str(dict(row))
		textobject.textLine(line)

	canvas_obj.drawText(textobject)
	canvas_obj.save()

	os.popen('evince ' + pdf)
 
if __name__ == '__main__':	 
	subprocess.call('clear',shell=True)

	print ("""\
                          | |  
 _ __ ___ _ __   ___  _ __| |_ 
| '__/ _ \ '_ \ / _ \| '__| __|
| | |  __/ |_) | (_) | |  | |_ 
|_|  \___| .__/ \___/|_|   \__|
         | |                   
         |_|   

Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Report

>>>Foram gerados os relatórios de utilização das tools em formato PDF na directoria /report<<<

	""") 

	report("chat")
	report("portscan")
 
