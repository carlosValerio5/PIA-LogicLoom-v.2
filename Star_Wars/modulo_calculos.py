from statistics import mode, mean, median
import json, requests
import psycopg2 as pg


#Funcion para calcular el planeta con mas personajes
def moda_planeta(connection):
    planetas = list()

    cursor = connection.cursor()

    cursor.execute("""
                   SELECT homeworld from people 
                   """)

    planetas = cursor.fetchall()
    print(planetas)

    # Calcular el planeta con más personajes usando la moda
    planeta_mascomun = mode(planetas)

    # Obtener el nombre del planeta correspondiente

    cursor.execute("""
                   SELECT planet from planets WHERE id_planet = %s 
                   """, (planeta_mascomun,))

    infoMasComun = cursor.fetchone()

    print("El planeta de nacimiento mas comun es: " , infoMasComun[0])


#Función para calcular la mediana del peso de los personajes de una especie
def mediana_peso(connection):

    #Consider implementing drop down menu to display different species
    species = "Droid"

    cursor = connection.cursor()


    #Query to extract mass from specified species
    cursor.execute("""
                    SELECT mass FROM people_species
                    JOIN (SELECT id_species from species
                    WHERE species = %s) n1 ON people_species.id_species = n1.id_species
                    JOIN people ON people_species.id_people = people.id_people;
                   """, (species, ))

    results = cursor.fetchall()
    weights = []
    for element in results:
        weights.append(element[0])
    medianWeights = median(weights)

    print(f"Median weight of the {species} species: {medianWeights} kgs")

  

#Función para calcular la media del diametro de los planetas en base a su clima
def media_clima(connection):
  cursor = connection.cursor()

  #implement menu for different climates
  clima_eleg = "arid"

  cursor.execute("""
                SELECT diameter FROM
                    (SELECT id_climate, id_planet FROM planet_climate) t1
                JOIN (SELECT id FROM climate WHERE name = %s) t2
                ON id_climate = id
                JOIN planets ON t1.id_planet = planets.id_planet;
                 """, (clima_eleg, ))

  result = cursor.fetchall()
  diameterClimate = []


  for diamResult in result:
    number = diamResult[0]

    #If the diameter is equal to zero it is considered as unknown
    if number>0:
        diameterClimate.append(number)

  if diameterClimate:
    media_diam = mean(diameterClimate)
    print(f"La media del diámetro de los planetas con clima '{clima_eleg}' es: {media_diam} km")
  else:
    print(f"No se encontraron planetas con el clima '{clima_eleg}' o no se encontraron diámetros válidos.")

