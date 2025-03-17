#!/usr/bin/python3

import psycopg2 as pg
import psycopg2.extras
import requests
import json
import asyncio
import aiohttp

import config
from modulo_graficas import calculateDensity
import re


def connectToDb():
    #Creating connection to postgresql database
    connection = pg.connect(database="starwars", user=config.username, password=config.password)

    #return connection object
    return connection

#make requests asynchronously to save time
async def fetch_data_async(url, endpoint, session):
    async with session.get(url + endpoint) as response:
        return await response.json()

def fetchData(connection):
    url = "https://swapi.dev/api/"
    endpoints = {"people", "planets", "species", "films"}
    cursor = connection.cursor()

    #commiting in batches to optimize time
    batch_size = 100
    people_data = []
    planet_data = []
    species_data = []
    films_data = []

    async def fetch_all_data():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for extension in endpoints:
                tasks.append(fetch_data_async(url, extension, session))
            return await asyncio.gather(*tasks)

    response_data = asyncio.run(fetch_all_data())

    #processing all data
    for index, extension in enumerate(endpoints):
        content = response_data[index]


        #number of elements in result
        count = content["count"]

        #number of pages for each endpoint
        pages = (count+9)//10

        for i in range(1, pages+1):
        
            page_content = requests.get(url+extension+"/?page=%s" % (i,)).json()
            results = page_content["results"]

            for element in results:
                if(extension == "people"):
                    person = element["name"]

                    #if mass is unknown set mass to 0 in db
                    try:
                        mass = float(element["mass"])
                    except ValueError:
                        mass = 0
                    #UPSERT query if row exists just update mass
                    #cursor.execute("""INSERT INTO people(person, mass)
                    #            VALUES(%s, %s)
                    #            ON CONFLICT (person) DO UPDATE SET
                    #            mass = %s
                    #            """, (person, mass, mass))
                    people_data.append((person, mass))

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
                    #cursor.execute("""
                    #               INSERT INTO planets(planet, diameter, population, density)
                    #               VALUES(%s, %s, %s, %s)
                    #               ON CONFLICT (planet) DO UPDATE SET
                    #               diameter = %s,
                    #              population = %s,
                    #              density = %s
                    #              """, (planet, diameter, population, density, diameter, population, density))
                    planet_data.append((planet, diameter, population, density))



                elif (extension == "species"):
                    species = element["name"]

                    #if register already exists do nothing
                    #cursor.execute("""
                    #               INSERT INTO species(species)
                    #               VALUES (%s)
                    #              ON CONFLICT (species) DO NOTHING
                    #              """, (species,))
                    species_data.append((species,))


                else:
                    film = element["title"]

                    #if register already exists do nothing
                    #cursor.execute("""
                    #               INSERT INTO films(film)
                    #               VALUES (%s)
                    #               ON CONFLICT (film) DO NOTHING
                    #               """, (film, ))
                    films_data.append((film, ))

    #update de people_species relationship table 

    #insert update in batches
    if people_data:
        insert_query = """
            INSERT INTO people(person, mass)
            VALUES %s
            ON CONFLICT (person) DO UPDATE SET mass = EXCLUDED.mass
        """
        pg.extras.execute_values (
                cursor, insert_query, people_data, template=None, page_size=100
                )

    if planet_data:
        insert_query = """
            INSERT INTO planets(planet, diameter, population, density)
            VALUES %s
            ON CONFLICT (planet) DO UPDATE SET diameter = EXCLUDED.diameter,
                                              population = EXCLUDED.population,
                                              density = EXCLUDED.density
        """
        pg.extras.execute_values(
                cursor, insert_query, planet_data, template=None, page_size=100
                )

    if species_data:
        insert_query = """
            INSERT INTO species(species)
            VALUES %s
            ON CONFLICT (species) DO NOTHING
        """
        pg.extras.execute_values(
                cursor, insert_query, species_data, template=None, page_size=100
                )

    if films_data:
        insert_query = """
            INSERT INTO films(film)
            VALUES %s
            ON CONFLICT (film) DO NOTHING
        """
        pg.extras.execute_values(
                cursor, insert_query,films_data, template=None, page_size=100
                )

    connection.commit()
    updateSpecies(connection)



#fetchData(connectToDb())

def updateSpecies(connection):
    url = "https://swapi.dev/api/people"
    cursor = connection.cursor()


    request = requests.get(url)
    content = json.loads(request.text)

    count = content["count"]

    #number of pages for each endpoint
    pages = int(count/10)
    if (count%10 != 0):
        pages+=1

    counter = 1
    for i in range(1, pages+1):
        response = requests.get(url+"/?page=" + str(i))
        content = response.json()

        results = content.get("results", [])
        for element in results:

            homeworld = int(re.findall(r'\d+', element["homeworld"])[0])


            person_url = element["url"]
            person_id = counter




            species = list(element["species"])

            for keySpecies in species:
                species_id = int(re.findall(r'\d+', keySpecies)[0])
                cursor.execute("""
                               INSERT INTO people_species (id_people, id_species)
                               VALUES (%s, %s) 
                               ON CONFLICT (id_people, id_species) DO NOTHING
                               """, (person_id, species_id))


            #updating homeworld field in people table to not waste resources in other function
            cursor.execute("""
                            UPDATE people
                            SET homeworld = (%s)
                            WHERE id_people = (%s)
                            """, (homeworld, person_id))

            #keeping track of the index of each person
            counter +=1

            
    connection.commit()


