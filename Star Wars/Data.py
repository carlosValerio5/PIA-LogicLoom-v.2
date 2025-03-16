#!/usr/bin/python3

import psycopg2 as pg
import requests
import json

import config
from modulo_graficas import calculateDensity


def connectToDb():
    #Creating connection to postgresql database
    connection = pg.connect(database="starwars", user=config.username, password=config.password)

    #return connection object
    return connection

def fetchData(connection):
    url = "https://swapi.dev/api/"
    endpoints = {"people", "planets", "species", "films"}
    cursor = connection.cursor()

    #reaching every endpoint required and storing data in db
    for extension in endpoints:
        response = requests.get(url+extension)
        content = json.loads(response.text)

        #number of elements in result
        count = content["count"]

        #number of pages for each endpoint
        pages = int(count/10)
        if (count%10 != 0):
            pages+=1
        for i in range(1, pages+1):
        
            response = requests.get(url+extension+"?page=%s" % (i,))
            content = json.loads(response.text)
            results = content["results"]

            for element in results:
                if(extension == "people"):
                    person = element["name"]

                    #if mass is unknown set mass to 0 in db
                    try:
                        mass = float(element["mass"])
                    except ValueError:
                        mass = 0
                    #UPSERT query if row exists just update mass
                    cursor.execute("""INSERT INTO people(person, mass)
                                VALUES(%s, %s)
                                ON CONFLICT (person) DO UPDATE SET
                                mass = %s""", (person, mass, mass))
                    connection.commit()

                elif (extension == "planets"):
                    planet = element["name"]
                    try:
                        diameter = float(element["diameter"])
                    except  ValueError:
                        diameter = 0                       
                    #Handle exception for planets with unknown population
                    try:
                        population = int(element["population"])
                    except ValueError:
                        population = None
                    density = calculateDensity(element)

                    #If register already exists update al fields except planet
                    cursor.execute("""
                                   INSERT INTO planets(planet, diameter, population, density)
                                   VALUES(%s, %s, %s, %s)
                                   ON CONFLICT (planet) DO UPDATE SET
                                   diameter = %s,
                                   population = %s,
                                   density = %s
                                   """, (planet, diameter, population, density, diameter, population, density))
                    connection.commit()



                elif (extension == "species"):
                    species = element["name"]

                    #if register already exists do nothing
                    cursor.execute("""
                                   INSERT INTO species(species)
                                   VALUES (%s)
                                   ON CONFLICT (species) DO NOTHING
                                   """, (species,))
                    connection.commit()


                else:
                    film = element["title"]

                    #if register already exists do nothing
                    cursor.execute("""
                                   INSERT INTO films(film)
                                   VALUES (%s)
                                   ON CONFLICT (film) DO NOTHING
                                   """, (film, ))
                    connection.commit()



#fetchData(connectToDb())
