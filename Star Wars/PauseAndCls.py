#!/usr/bin/env python3

import os

def limpiarP(): #? Metodo para limpiar pantalla
    sistemaOp = os.name
    if sistemaOp == "nt":
        os.system('cls')
    elif sistemaOp == "posix":
        os.system('clear')
def pausa(): #? Metodo para pausar pantalla hasta darle clic
    sistemaOp = os.name
    if sistemaOp == "nt": 
        os.system("pause")
    elif sistemaOp == "posix":
        input("Presiona Enter para continuar...")



