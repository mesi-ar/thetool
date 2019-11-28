#!/usr/bin/python3

import os
import sqlite3
from datetime import datetime

dbName = "chat.db"
timestamp = datetime.now()

conn=sqlite3.connect(dbName)

conn.execute("insert into chat(ip, name,type,msg,timestamp) values (?,?,?,?,?)", ("12.2.2.1","zeze","server", "ola", datetime.now()))

conn.commit()
conn.close()
