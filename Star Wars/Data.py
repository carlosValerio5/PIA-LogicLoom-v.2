#!/usr/bin/python3

import psycopg2 as pg

import config

connection = pg.connect(database="starwars", user=config.username, password=config.password)

cursor = connection.cursor()
cursor.execute("SELECT * from people")

record = cursor.fetchall()

print(record)
