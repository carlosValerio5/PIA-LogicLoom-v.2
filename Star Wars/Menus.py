#!/usr/bin/env python3
import time
import PauseAndCls 
from colorama import Fore, Style, init 

init()


def MostrarMenu():
  PauseAndCls.limpiarP() # Se usó la función limpiarP
  print("Hola Bienvenido al programa")
  op = """Opciones:
  1.- Consulta de datos
  2.- Historial
  3.- Graficas y Calculos
  4.- Salir\n"""
  print(op)


def lecturaOp():
  MostrarMenu()
  try:  # Proceso de validar que el usuario ponga los datos correctos
      while True:
          op = int(input("Selecciona una opción del 1 al 4: "))
          if op > 0 and op < 5:
              break
  except ValueError:
      print(Fore.RED + Style.BRIGHT + "Solo se aceptan números enteros" + Style.RESET_ALL)
      time.sleep(2)
      op = lecturaOp()
  except Exception as error:
      print(error)
      op = lecturaOp()
  finally:
      return op


def menu2():  # Imprimir la el menú para saber la búsqueda
  PauseAndCls.limpiarP()
  opB = """Opciones de búsqueda:
  1.- Búsqueda por personaje
  2.- Búsqueda por Especie
  3.- Búsqueda por Planeta
  """
  print(opB)


def lecturaOpB():  # Función para validar opción de búsqueda
  menu2()
  try:
      while True:
          op = int(input("Selecciona una opción del 1 al 3: "))
          if op > 0 and op < 4:
              break
  except ValueError:
      print(Fore.RED + Style.BRIGHT + "Solo se aceptan números enteros" + Style.RESET_ALL)
      time.sleep(2)
      op = lecturaOpB()
  except Exception as error:
      print(error)
      op = lecturaOpB()
  finally:
      return op


def menucalgraf():
  try:
      while True:
          PauseAndCls.limpiarP()
          print('''Que desea hacer?
              1.- Calculos
              2.- Graficas''')
          value = int(input(":"))
          if value != 1 and value != 2:
              print("Ingrese un valor entre 1 y 2")
              PauseAndCls.pausa()
              continue
          break
  except ValueError:
      print("Ingrese un valor numerico")
      PauseAndCls.pausa()
      value = menucalgraf()
  return value

def menucalcs():
  try:
      while True:
          PauseAndCls.limpiarP()
          print('''1)Mediana peso de personajes
      2) Moda de planetas con mas nacimientos de personajes
      3)Media de diametro de planetas''')
          var = int(input(":"))
          if var != 1 and var != 2 and var != 3:
              print("Ingrese un numero entre 1 y 3")
              PauseAndCls.pausa()
              continue
          break
  except ValueError:
      print("Ingrese un valor numerico")
      PauseAndCls.pausa()
      var = menucalcs()
  return var

def menugrafs():
  try:
      while True:
          PauseAndCls.limpiarP()
          print('''1)Grafica de Numero de Peliculas
          2)Grafica de Porcentaje de Especies
          3)Grafica de Densidad Poblacional''')
          var = int(input(":"))
          if var != 1 and var != 2 and var != 3:
              print("Ingrese un numero entre 1 y 3")
              PauseAndCls.pausa()
              continue
          break
  except ValueError:
      print("Ingrese un valor numerico")
      PauseAndCls.pausa()
      var = menugrafs()
  return var