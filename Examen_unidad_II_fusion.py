# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 11:22:10 2021

@author: KEVIN
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
# Para leer shapefiles
import shapefile
import pygeoif

import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo



#Establecer ventana
vent = tk.Tk()
vent.geometry('1400x700')

vent.title('Calculo de Zonas Inundadas')    #agregar titulo
vent.config(bg= 'gainsboro')


###################################################### Widget 1 ################################################################################
## Agregar etiqueta 1
etiq1 = tk.Label(vent, text='1. Seleciona la imagen a utilizar', bg='silver',  fg='black', font = 'Helvetica 10')
etiq1.grid(row = 0, column = 1, pady = (3))

## caja de texo 1
textResult1 = tk.Text(vent, height = 1, font = 'Helvetica 10', bg = 'white', fg = 'black', highlightthickness = 3)                                
textResult1.grid(row = 2, column = 1, padx = (50,50))


#funcion para abrir imagen
def abrir_imagen():
    global imagen_abierta
    imagen_abierta=filedialog.askopenfilename(initialdir = "/", title = "Seleccione la imagen",filetypes = (("zip files","*.zip"),("all files","*.*")))
    #print (imagen_abierta)
    textResult1.insert(tk.END, imagen_abierta)
    
    #Cargar imagenes
    path_to_sentinel_data = imagen_abierta
    global product
    product = ProductIO.readProduct(path_to_sentinel_data)

    #Leer y mostrar la informaciónd de la imagen
    width = product.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product.getSceneRasterHeight()
    print("Height: {} px".format(height))
    name = product.getName()
    print("Name: {}".format(name))
    band_names = product.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))
    

#Agregar boton 1
boton1 = tk.Button(text="Seleccionar imagen", font = 'Helvetica 10',  bg="white",command=abrir_imagen)
boton1.grid(row = 1, column = 1, padx = (10,10))


######################################## Crear una funcion para mostrar el producto en una #################################
def plotBand(product, band, vmin, vmax):
    band = product.getBand(band)
    w = band.getRasterWidth()
    h = band.getRasterHeight()
    print(w, h)
    band_data = np.zeros(w * h, np.float32)
    band.readPixels(0, 0, w, h, band_data)
    band_data.shape = h, w
    width = 12
    height = 12
    plt.figure(figsize=(width, height))
    imgplot = plt.imshow(band_data, cmap=plt.cm.binary, vmin=vmin, vmax=vmax)
    


###################################################### PRE-PROCESAMIENTO ###################################################

##################################################### Widget 2 ###################################################################################

#Agregar etiqueta 2
etiq2 = tk.Label(vent, text='2. Seleciona el Shapefile de la zona de estudio', font = 'Helvetica 10', bg='silver',  fg='black')
etiq2.grid(row = 3, column = 1)

#caja de texo 1
textResult2 = tk.Text(vent, height = 1, font = 'Helvetica 10', bg = 'white', fg = 'black', highlightthickness = 3)                                     
textResult2.grid(row = 5, column = 1, padx = (100,100))


#funcion para abrir imagen
def abrir_shape():
    shape_abierto=filedialog.askopenfilename(initialdir = "/", title = "Seleccione shapefile",filetypes = (("shapefile files","*.shp"), ("all files","*.*")))
    print (shape_abierto)
    textResult2.insert(tk.END, shape_abierto)
    ############################### Recortar la imagen
    r = shapefile.Reader(shape_abierto)
    g=[]
    for s in r.shapes():
        g.append(pygeoif.geometry.as_shape(s))
    m = pygeoif.MultiPoint(g)
    global wkt
    wkt = str(m.wkt).replace("MULTIPOINT", "POLYGON(") + ")"
    

#Agregar boton 2
boton2 = tk.Button(text="Seleccione el shapefile ", font = 'Helvetica 10', bg="white", command = abrir_shape)
boton2.grid(row = 4, column = 1)


################################################### Widget 3 ##################################################

#Agregar etiqueta 3
etiq3 = tk.Label(vent, text='3. Proceda a pre-procesar la imagen', font = 'Helvetica 10', bg='silver',  fg='black')
etiq3.grid(row = 6, column = 1)

def pre_proc():
    
    ############################## Aplicar correccion orbital
    global HashMap
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', '3')
    parameters.put('continueOnFail', 'false')
    global apply_orbit_file
    apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, product)
        
    ############################### Usar el shapefile para cortar la imagen
    SubsetOp = snappy.jpy.get_type('org.esa.snap.core.gpf.common.SubsetOp')
    bounding_wkt = wkt
    geometry = WKTReader().read(bounding_wkt)
    HashMap = snappy.jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', geometry)
    product_subset = snappy.GPF.createProduct('Subset', parameters, apply_orbit_file)

    ############################# Mostrar las dimensiones de la imagen
    width = product_subset.getSceneRasterWidth()
    print("Width: {} px".format(width))
    height = product_subset.getSceneRasterHeight()
    print("Height: {} px".format(height))
    band_names = product_subset.getBandNames()
    print("Band names: {}".format(", ".join(band_names)))
    band = product_subset.getBand(band_names[0])
    print(band.getRasterSize())
    #plotBand(product_subset, "Intensity_VV", 0, 100000)

    ############################ Aplicar la calibracion de la imagen
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', 'Intensity_VV')
    parameters.put('selectedPolarisations', "VV")
    parameters.put('outputImageScaleInDb', False)
    product_calibrated = GPF.createProduct("Calibration", parameters, product_subset)
    #plotBand(product_calibrated, "Sigma0_VV", 0, 1)

    ########################### Aplicar el filtro Speckle
    filterSizeY = '5'
    filterSizeX = '5'
    parameters = HashMap()
    parameters.put('sourceBands', 'Sigma0_VV')
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', filterSizeX)
    parameters.put('filterSizeY', filterSizeY)
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')
    speckle_filter = snappy.GPF.createProduct('Speckle-Filter', parameters, product_calibrated)
    #plotBand(speckle_filter, 'Sigma0_VV', 0, 1)

    ############################ Aplicar la correccion del terremo
    parameters = HashMap()
    parameters.put('demName', 'SRTM 3Sec')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('sourceBands', 'Sigma0_VV')
    global speckle_filter_tc
    speckle_filter_tc = GPF.createProduct("Terrain-Correction", parameters, speckle_filter)
    plotBand(speckle_filter_tc, 'Sigma0_VV', 0, 0.1)
    
    message = 'Preproceso finalizado con exito'
    showinfo('¡Finish!', message)
    
#Agregar boton 3
boton3 = tk.Button(text="Preprocesar la imagen", font = 'Helvetica 10', bg="white", command = pre_proc)
boton3.grid(row = 7, column = 1)

################################################### Widget 4 ##################################################

#Agregar etiqueta 4
etiq4 = tk.Label(vent, text='4. Defina el umbral de la mascara de agua', font = 'Helvetica 10', bg='silver',  fg='black')
etiq4.grid(row = 10, column = 1)

#Agregar caja de texto
global umbral
umbral = tk.Entry(vent, font= 'Helvetica 10', justify = 'center', highlightthickness = 3)
umbral.grid(row = 11, column = 1, pady = (3))


def masc():
    texto = '(Sigma0_VV < '+ umbral.get() +') ? 1 : 0'
    ############################ Crear una mascara binaria para la inundacion
    parameters = HashMap()
    BandDescriptor = snappy.jpy.get_type('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor')
    targetBand = BandDescriptor()
    targetBand.name = 'Sigma0_VV_Flooded'
    targetBand.type = 'uint8'
    targetBand.expression = texto
    targetBands = snappy.jpy.array('org.esa.snap.core.gpf.common.BandMathsOp$BandDescriptor', 1)
    targetBands[0] = targetBand
    parameters.put('targetBands', targetBands)
    global flood_mask
    flood_mask = GPF.createProduct('BandMaths', parameters, speckle_filter_tc)
    plotBand(flood_mask, 'Sigma0_VV_Flooded', 0, 1)
    

#Agregar boton 4
boton4 = tk.Button(text="Aplicar la mascara", font = 'Helvetica 10', bg="white", command = masc)
boton4.grid(row = 12, column = 1, pady =(3))


################################################## Widget 5 #####################################################

#Agregar etiqueta 5
etiq5 = tk.Label(vent, text='5. Crea la imagen GeoTIFF a partir del umbral seleccionado', font = 'Helvetica 10', bg='silver',  fg='black')
etiq5.grid(row = 13, column = 1)

def guardar():
    ProductIO.writeProduct(flood_mask, imagen_abierta, 'GeoTIFF')
    #os.path.exists("C:/CTE_334/resul9/ETA.tif")

boton5 = tk.Button(text="Crear el archivo", font = 'Helvetica 10', bg="white", command = guardar)
boton5.grid(row = 14, column = 1)

mapa = tk.Canvas(vent, width = 500, height = 600, bg = 'white', highlightthickness = 10)
mapa.grid(row = 0, column = 2, rowspan = 16, pady =(30))

vent.mainloop()









