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

        #list of tuples with name and amount
        pelis.append((names[i], cursor.fetchone()[0]))
  

    print(pelis)
    cursor.close()
    return pelis

def mostrar_graficoApa(connection):

    #Get data for al species
    results  = obtener_datosEsp(connection)


    #Sort by amount in descending order
    results.sort(key = lambda tup: tup[1], reverse = True)

    #only showing the 10 characters with the most appearances
    top_10 = results[:10]


    nombres = []
    pelis = []

    for i in range(10):
        nombres.append(top_10[i][0])
        pelis.append(top_10[i][1])

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

def obtener_datosPln(cursor):
    planetas_data= list()

    #Retrieve only the first 18 planets
    cursor.execute("""
                   SELECT * from planets
                   LIMIT 18 OFFSET 0
                   """)

    planetas_data = cursor.fetchall()


    """for i in range(1,8):
        url= "http://swapi.dev/api/planets/"+str(i)+'/'
        response = requests.get(url)

        infoPlaneta = json.loads(response.text)
        planetas_data.append(infoPlaneta)"""
        
    return planetas_data

def mostrar_graficaDen(connection):

    cursor = connection.cursor()

    planetas_data = obtener_datosPln(cursor)
    plan = list()
    den_pob = list()
    planFil = list()

    for elem in planetas_data:
        if elem[3] != None and elem[2] != 0:
            planFil.append({"diameter": elem[2], "population" : elem[3], "name": elem[1]})

    for planeta in planFil:
        ar = 3.14*(float(planeta['diameter'])/2)**2
        den = float(planeta['population']) / ar
        planeta['density'] = den

        plan.append(planeta['name'])
        den_pob.append( planeta['density'])

    plt.axis(ymin=0, ymax=18)
    plt.scatter(plan, den_pob, color = 'red')
    plt.yscale('log')
    plt.ylim(bottom=min(den_pob), top=max(den_pob))
    plt.xlabel('Planetas', fontdict={'family': 'serif', 'color':  '#DDA0DD', 'weight': 'bold', 'size': 14})
    plt.ylabel('Densidad poblacional',fontdict={'family': 'serif', 'color':  '#DDA0DD', 'weight': 'bold', 'size': 14})
    plt.title('Densidad Poblacional de Planetas de Star Wars',fontdict={'family': 'monospace', 'color':  '#663399', 'weight': 'bold', 'size': 16})
    plt.show()
    cursor.close()

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




