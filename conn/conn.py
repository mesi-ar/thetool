#!/usr/bin/python3

import os
import sqlite3, subprocess
import geoip2.database
from datetime import datetime
#graph https://matplotlib.org/tutorials/introductory/lifecycle.html#sphx-glr-tutorials-introductory-lifecycle-py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def conn2bd():
    response = os.popen('netstat -4tnp')
    for line in response.readlines()[2:]:
        print (line)
        words = line.split()
        
        #foreign
        foreign = words[4] 
        foreign = foreign.split(":")

        #city
        try:
            ip_geo = bdgeoip.city(foreign[0])
            city = ip_geo.city.names['en'] + ", " + ip_geo.country.iso_code
            country = ip_geo.country.names['en']
        except:
            city = "ND"
            country = "ND"
            pass
    
        #program
        program = words[6]
        program = program.split("/")

        connbd=sqlite3.connect(dbName)
        connbd.execute("insert into conn (proto, local, foreig, state, program, city, country, timestamp) values (?,?,?,?,?,?,?,?)", (words[0], words[3], foreign[0], words[5], program[1], city, country, datetime.now())) 
        connbd.commit()
        connbd.close()

def bd(dbName):
    dbIsNew = not os.path.exists(dbName)

    connbd=sqlite3.connect(dbName)

    if dbIsNew:
        sql = """create table conn (
        id      integer primary key autoincrement not null,
        proto   text,
        local   text,
        foreig     text,
        program     text,
        state   text,
        city    text,
        country    text,
        timestamp timestamp);"""

        connbd.executescript(sql)
        connbd.commit()
        connbd.close()
        print ("Base dados criado com sucesso\n")

def graph(column):
    y = []#number occurencies
    x = [] #list of column

    connbd=sqlite3.connect(dbName)

    #country list
    columnsql = "SELECT DISTINCT " + column + " FROM conn"
    countrycur = connbd.cursor()
    countrycur.execute(columnsql)
    countryrows = countrycur.fetchall()
    for c in countryrows:
        c = str(c)
        #remove bad chars
        bad_chars = ["(",")",",","'","[","]"]
        for i in bad_chars : 
            c = c.replace(i, '')
        #count ocurrencies
        ocurrsql = "SELECT count (" + column + ") from conn where " + column + " = '" + c + "'"
        occurcur = connbd.cursor()
        occurcur.execute(ocurrsql)
        occurrows = occurcur.fetchall()
        occurrows = str(occurrows)
        for i in bad_chars : 
            occurrows = occurrows.replace(i, '')
        x.append(c)
        y.append(int(occurrows))

    #print graph 
    fig, ax = plt.subplots()
    ax.barh(x, y)
    ax.set_title('Occurrencias por ' + column)
    plt.style.use('fivethirtyeight')

    plt.show()
    
   
if __name__ == '__main__':
    subprocess.call('clear',shell=True)
   
    print ("""\
  ___ ___  _ __  _ __  
 / __/ _ \| '_ \| '_ \ 
| (_| (_) | | | | | | |
 \___\___/|_| |_|_| |_|
                       
Instituto Politécnico de Beja
Mestrado em Engenharia de Segurança Informática 2019/20
Disciplina: Linguagens de Programação Dinâmicas
Aluno: Afonso Rodrigues [19025]
Tool: Conn

    """)
    
    #bd sqlite
    dbName = "./conn/conn.db"
    bd(dbName)

    #bd geoip
    bdgeoip = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')

    while True:
        a = input("Queres consultar as ligações activas? (Sim | Nao)\n")
        if a in ["s","S","SIM","Sim","sim"]:
            conn2bd()
        else:
            break 

    #graph
    while True:
        r = input("Queres gerar um grafico de ocurrencias? (nao | protocolo | ip | programa | pais)\n")
        if r == "nao":
            break
        elif r == "pais":
            graph("country")
        elif r == "protocolo":
            graph("proto")
        elif r == "ip":
            graph("foreig")
        elif r == "programa":
            graph("program")
        else:
            print ("\nEscreve >>> nao OU protocolo OU ip OU programa OU pais <<<\n")