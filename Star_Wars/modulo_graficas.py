import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import psycopg2 as pg
import psycopg2.extras


#Grafica de barras
def obtener_datosEsp(connection):
    names = list()
    pelis = list()

    cursor = connection.cursor()
    cursor.execute("""
                   SELECT person, id_people FROM people 
                   """)
    results = cursor.fetchall()

    for name in results:
        names.append(name[0])

    for i in range(len(names)):
        cursor.execute("""
                SELECT count(*) 
                AS exact_count 
                FROM people_films WHERE id_people = %s;
                       """, (results[i][1], ))
        pelis.append(cursor.fetchone()[0])
  

    cursor.close()
    return names, pelis

def mostrar_graficoApa(connection):
    nombres, pelis = obtener_datosEsp(connection)
    x = np.array(nombres)
    y = np.array(pelis)
    mycolors = ['#FF6F61', '#6B4226', '#99B2DD', '#D9BF77', '#52796F',
                '#E4B4A5', '#3E4095', '#B1A296', '#779ECB', '#F9A875']
    plt.bar(x, y, color=mycolors)
    plt.title('Apariciones en peliculas', fontdict={'family': 'monospace', 'color':  'lightpink', 'weight': 'bold', 'size': 16})
    plt.xticks(rotation='vertical')
    plt.xlabel('Personajes', fontdict={'family': 'serif', 'color':  '#DB7093', 'weight': 'bold', 'size': 14})
    plt.ylabel('Numero de peliculas',fontdict={'family':'serif','color':'#DB7093','weight': 'bold', 'size': 14})
    plt.show()

#Grafica de Pastel
def get_species(cursor):
    especies = []

    cursor.execute("""
                   SELECT id_species FROM species 
                   """)
    especies = cursor.fetchall()



    """while url:
        response = requests.get(url)
        data = response.json()
        especies.extend(data['results'])
        url = data['next']"""

    return especies

def get_amount(diccionario):
    return diccionario['amount']

def mostrar_graficoEsp(connection):

    cursor = connection.cursor()

    species_data = get_species(cursor)
    
    cursor.execute("""
                   SELECT species FROM species
                   """)
    
    namesSpecies = cursor.fetchall()

    counts = []


    for name in namesSpecies:
        cursor.execute("""
                    SELECT  count(*) from people_species
                    JOIN (SELECT species.id_species FROM species WHERE species = %s) ps on people_species.id_species = ps.id_species;
                    """, name)
        result = cursor.fetchone()
        counts.append({'name' : name[0], 'amount' : result[0]})

    #info= list()

    ordered_species = sorted(counts, key = get_amount, reverse = True)

    top_5 = ordered_species[:5]

    species_names = list()
    amount_characters = list()

    for species in top_5:
        species_names.append(species['name'])
        amount_characters.append(species['amount'])
                               
    y = np.array(amount_characters)
    colores = ['#8FB369', '#6A9EC3', '#F7CD5E', '#E8A5C6', '#D9D9D9']

    plt.pie(y, labels= species_names, autopct='%1.1f%%', shadow= True, colors= colores)
    plt.title('Species Frequency', fontdict={'family': 'monospace', 'color':  'lightcoral', 'weight': 'bold', 'size': 16})
    plt.show()
    cursor.close()


#Grafica de dispersion

def obtener_datosPln():
    planetas_data= list()
    for i in range(1,8):
        url= "http://swapi.dev/api/planets/"+str(i)+'/'
        response = requests.get(url)

        infoPlaneta = json.loads(response.text)
        planetas_data.append(infoPlaneta)
        
    return planetas_data

def mostrar_graficaDen():
    planetas_data = obtener_datosPln()
    plan = list()
    den_pob = list()
    planFil = list()

    for dicc in planetas_data:
        if dicc['population'] != 'unknown' and dicc['diameter'] != '0' and dicc['population'] != '0' and dicc['diameter'] != 'unknown':
            planFil.append(dicc)

    for planeta in planFil:
        ar = 3.14*(float(planeta['diameter'])/2)**2
        den = float(planeta['population']) / ar
        planeta['densidad'] = den

        plan.append(planeta['name'])
        den_pob.append( planeta['densidad'])

    plt.axis(ymin=0, ymax=18)
    plt.scatter(plan, den_pob, color = 'red')
    plt.yscale('log')
    plt.ylim(bottom=min(den_pob), top=max(den_pob))
    plt.xlabel('Planetas', fontdict={'family': 'serif', 'color':  '#DDA0DD', 'weight': 'bold', 'size': 14})
    plt.ylabel('Densidad poblacional',fontdict={'family': 'serif', 'color':  '#DDA0DD', 'weight': 'bold', 'size': 14})
    plt.title('Densidad Poblacional de Planetas de Star Wars',fontdict={'family': 'monospace', 'color':  '#663399', 'weight': 'bold', 'size': 16})
    plt.show()

def calculateDensity(planet):

    try:
        diameter = float(planet["diameter"])
    except ValueError:
        return 0;

    area = 3.14*(float(planet['diameter'])/2)**2

    try:
        density = float(planet['population']) / area
    except ValueError:
        density = 0
    except ZeroDivisionError:
        density = 0
    return density




