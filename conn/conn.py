#!/usr/bin/python3

import os
import sqlite3
import subprocess
import geoip2.database
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def conn2bd(): #funcao de avaliaão das ligações existentes. actualiza a bd com a informação recolhida
    response = os.popen('netstat -4tnp')
    for line in response.readlines()[2:]:#começa na 2a linha para excluir o cabeçalho
        print (line)
        words = line.split()

        #definição de ip externo
        foreign = words[4]
        foreign = foreign.split(":")

        #identificação da localizaçao do ip externo
        try:
            ip_geo = bdgeoip.city(foreign[0])
            city = ip_geo.city.names['en'] + ", " + ip_geo.country.iso_code
            country = ip_geo.country.names['en']
        except BaseException:
            city = "ND"
            country = "ND"
            pass

        #identificaçao do programa que realizou a comunicação
        try:
            program = words[6]
            program = program.split("/")
            program = program[1]

        except BaseException:
            program = "ND"
            pass

        #actualização da bd
        connbd = sqlite3.connect(dbName)
        connbd.execute(
            "insert into conn (proto, local, foreig, state, program, city, country, timestamp) values (?,?,?,?,?,?,?,?)",
            (words[0],
             words[3],
                foreign[0],
                words[5],
                program,
                city,
                country,
                datetime.now()))
        connbd.commit()
        connbd.close()


def bd(dbName):#função de criação da base de dados
    dbIsNew = not os.path.exists(dbName)

    connbd = sqlite3.connect(dbName)

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


def graph(column):#função de desenho do grafico
    y = []  #numero de ocorrencias
    x = []  #colunas

    connbd = sqlite3.connect(dbName)

    columnsql = "SELECT DISTINCT " + column + " FROM conn" #identifica valores unicos para a coluna sobre a qual se quer fazer o grafico
    ccur = connbd.cursor()
    ccur.execute(columnsql)
    crows = ccur.fetchall()
    for c in crows:#para cada valor da coluna, remove caracteres indesejados, conta as ocorrencias e alimenta as variaveis que irao ser x e y do grafico
        c = str(c)
        #remove caracteres indesejados
        bad_chars = ["(", ")", ",", "'", "[", "]"]
        for i in bad_chars:
            c = c.replace(i, '')
        #conta ocorrencias
        ocurrsql = "SELECT count (" + column + \
            ") from conn where " + column + " = '" + c + "'"
        occurcur = connbd.cursor()
        occurcur.execute(ocurrsql)
        occurrows = occurcur.fetchall()
        occurrows = str(occurrows)
        for i in bad_chars:
            occurrows = occurrows.replace(i, '')
        #alimenta x e y
        x.append(c)
        y.append(int(occurrows))

    #gera o grafico de barras
    fig, ax = plt.subplots()
    ax.barh(x, y)
    ax.set_title('Occurrencias por ' + column)
    plt.style.use('fivethirtyeight')

    plt.show()


if __name__ == '__main__':
    subprocess.call('clear', shell=True)

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

    # bd sqlite
    dbName = "./conn/conn.db"
    bd(dbName)

    # bd geoip
    bdgeoip = geoip2.database.Reader('./geoip/GeoLite2-City.mmdb')

    while True: #ciclo de consulta das ligações activas e actualização da bd
        a = input("Queres consultar as ligações activas? (Sim | Nao)\n")
        if a in ["s", "S", "SIM", "Sim", "sim"]:
            conn2bd()
        else:
            break

    #ciclo de geraçao de grafico
    while True:
        r = input(
            "Queres gerar um grafico de ocurrencias? (nao | protocolo | ip | programa | pais)\n")
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
