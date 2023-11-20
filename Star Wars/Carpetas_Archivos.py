#!/usr/bin/env python3
import os


def DireccionJoin(texto): #Funcion para juntar la direccion 
    ruta = os.getcwd()
    direccion = os.path.join(ruta, texto)
    return direccion