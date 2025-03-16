import requests
import json
import numpy as np
import matplotlib.pyplot as plt

#Grafica de barras
def obtener_datosEsp():
    nombres = list()
    pelis = list()

    for i in range(1, 11):  # Pongan un número pequeño, puede tardar mucho
        url = "http://swapi.dev/api/people/" + str(i) + '/'
        response = requests.get(url)

        if response.status_code != 200:  # Si consultaramos alguna que no existe, es mejor terminar
            break

        infoPersonaje = json.loads(response.text)
        nombres.append(infoPersonaje["name"])

        num_apariciones = len(infoPersonaje["films"])
        pelis.append(num_apariciones)

    return nombres, pelis

def mostrar_graficoApa():
    nombres, pelis = obtener_datosEsp()
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
def obtener_especies(url):
    especies = []

    while url:
        response = requests.get(url)
        data = response.json()
        especies.extend(data['results'])
        url = data['next']

    return especies

def obtener_cantidad(diccionario):
    return diccionario['cantidad']

def mostrar_graficoEsp():
    url_especies = 'https://swapi.dev/api/species/'
    especies_data = obtener_especies(url_especies)

    info= list()
    for especie in especies_data:
        info.append({'nombre': especie['name'],
                 'cantidad': len(especie['people'])})

    especies_ordenadas = sorted(info, key = obtener_cantidad, reverse = True)

    top_5 = especies_ordenadas[:5]

    nombres_especies = list()
    cantidad_personajes = list()

    for especie in top_5:
        nombres_especies.append(especie['nombre'])
        cantidad_personajes.append(especie['cantidad'])
                               
    y = np.array(cantidad_personajes)
    colores = ['#8FB369', '#6A9EC3', '#F7CD5E', '#E8A5C6', '#D9D9D9']

    plt.pie(y, labels= nombres_especies, autopct='%1.1f%%', shadow= True, colors= colores)
    plt.title('Frecuencia de Especies', fontdict={'family': 'monospace', 'color':  'lightcoral', 'weight': 'bold', 'size': 16})
    plt.show()


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
    area = 3.14*(float(planet['diameter'])/2)**2

    try:
        density = float(planet['population']) / area
    except ValueError:
        density = 0
    return density
