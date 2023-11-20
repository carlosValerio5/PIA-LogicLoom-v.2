from statistics import mode, mean, median
import json, requests

#Funcion para calcular el planeta con mas personajes
def moda_planeta():
    planetas = list()
    for i in range(1, 5):  
        url = "http://swapi.dev/api/people/" + str(i) + '/'
        response = requests.get(url)

        # Si consultáramos alguna que no existe, es mejor terminar
        if response.status_code != 200:
            break

        infoPersonaje = json.loads(response.text)

        # Asegurarse de que el personaje tenga un planeta de origen antes de
        # agregar a la lista
        if "homeworld" in infoPersonaje:
            planetas.append(infoPersonaje["homeworld"])

    # Calcular el planeta con más personajes usando la moda
    planeta_mascomun = mode(planetas)

    # Obtener el nombre del planeta correspondiente
    planeta_response = requests.get(planeta_mascomun)
    if planeta_response.status_code == 200:
        planeta_info = json.loads(planeta_response.text)
        print("El planeta de nacimiento más común es:", planeta_info["name"])
    else:
        print("No se pudo obtener información del planeta.")

#Función para calcular la mediana del peso de los personajes de una especie
def mediana_peso():
    especie = "Droid"

    url = f"https://swapi.dev/api/species/?search={especie}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error al hacer la solicitud a la API de Star Wars. Código de estado {response.status_code}")
        return

    data = response.json()
    species = data.get('results', [])

    if not species:
        print(f"No se encontró la especie {especie}.")
        return

    especie_url = species[0]['url']
    response = requests.get(especie_url)

    if response.status_code != 200:
        print(f"Error al obtener información de la especie {especie}.")
        return

    especie_data = response.json()
    people_urls = especie_data.get('people', [])

    peso_especie = []

    for personaje_url in people_urls:
        response = requests.get(personaje_url)
        if response.status_code != 200:
            print(f"Error al obtener información del personaje desde {personaje_url}.")
            continue

        personaje_data = response.json()
        peso = personaje_data.get('mass')

        try:
            if peso != "unknown":
                peso = float(peso)
                peso_especie.append(peso)
        except (ValueError, TypeError):
            pass

    if peso_especie:
        mediana = median(peso_especie)
        print(f"Mediana del peso de los personajes de la especie {especie}: {mediana} kg")
    else:
        print(f"No se encontraron pesos válidos para los personajes de la especie {especie}.")

#Función para calcular la media del diametro de los planetas en base a su clima
def media_clima():
  clima_eleg = "Arid"
  url = "https://swapi.dev/api/planets/"
  planet_clim = []

  while url:
    response = requests.get(url)

    if response.status_code != 200:
      print(f"Error al hacer la solicitud a la API de Star Wars. Código de estado: {response.status_code}")
      return
    
    data = response.json()

    for planeta in data['results']:
      if clima_eleg.lower() in planeta['climate'].lower():
        diameter = planeta['diameter']
        if diameter != 'unknown':
          planet_clim.append(float(diameter))

    url = data.get('next')

  if planet_clim:
    media_diam = mean(planet_clim)
    print(f"La media del diámetro de los planetas con clima '{clima_eleg}' es: {media_diam} km")
  else:
    print(f"No se encontraron planetas con el clima '{clima_eleg}' o no se encontraron diámetros válidos.")
