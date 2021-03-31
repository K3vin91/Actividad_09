# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:55:00 2021

@author: KEVIN
"""
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


vent = tk.Tk()                 #crear venytana
vent.geometry('800x800')

vent.title('Calculo de zonas inundadas')    #agregar titulo
vent.config(bg= 'silver')

###########################################################################
#Agregar etiqueta 1
etiq1 = tk.Label(vent, text='elegir directorio', bg='silver',  fg='black')
etiq1.grid(row = 0, column = 0)

#Agregar caja 1
archivo = fd.askopenfilename(initialdir="C:/Users/KEVIN/Documents", tittle="select file", filetypes=(("png files","*.png"),("all files","*.*")))

 
vent.mainloop()