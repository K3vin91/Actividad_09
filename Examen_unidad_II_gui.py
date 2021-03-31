# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:55:00 2021

@author: KEVIN
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os

#Establecer ventana
vent = tk.Tk()
vent.geometry('700x800')

vent.title('Calculo de Zonas Inundadas')    #agregar titulo
vent.config(bg= 'silver')


###################################################### Widget 1 ##############################################

#Agregar etiqueta 1
etiq1 = tk.Label(vent, text='1. Seleciona la imagen a utilizar', bg='silver',  fg='black', font = 'Helvetica 8')
etiq1.grid(row = 0, column = 1)

#caja de texo 1
textResult = tk.Text(vent, height = 1, font = 'Helvetica 8', bg = 'white', fg = 'black', highlightthickness = 3)         #cuadro de texto                                
textResult.grid(row = 2, column = 1, padx = (50,50))

#funcion para abrir imagen
def abrir_imagen():
    archivo_abierto=filedialog.askopenfilename(initialdir = "/",
                title = "Seleccione la imagen",filetypes = (("jpeg files","*.jpg"),
                ("all files","*.*")))
    print (archivo_abierto)
    textResult.insert(tk.END, archivo_abierto)

boton1 = Button(text="Seleccionar imagen", font = 'Helvetica 8',  bg="white",command=abrir_imagen)
boton1.grid(row = 1, column = 1, padx = (10,10))


##################################################### Widget 2 ###############################################

#Agregar etiqueta 2
etiq2 = tk.Label(vent, text='2. Seleciona un Shapefile', font = 'Helvetica 8', bg='silver',  fg='black')
etiq2.grid(row = 3, column = 1)

#caja de texo 1
textResult = tk.Text(vent, height = 1, font = 'Helvetica 8', bg = 'white', fg = 'black', highlightthickness = 3)         #cuadro de texto                                
textResult.grid(row = 5, column = 1, padx = (100,100))

#funcion para abrir imagen
def abrir_shape():
    archivo_abierto=filedialog.askopenfilename(initialdir = "/",
                title = "Seleccione shapefile",filetypes = (("jpeg files","*.jpg"),
                ("all files","*.*")))
    print (archivo_abierto)
    textResult.insert(tk.END, archivo_abierto)

boton1 = Button(text="Seleccionar imagen", font = 'Helvetica 8', bg="white", command = abrir_shape)
boton1.grid(row = 4, column = 1)


vent.mainloop()











