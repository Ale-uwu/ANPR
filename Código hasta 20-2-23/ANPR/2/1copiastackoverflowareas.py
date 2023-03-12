# Se importan las librerías necesarias para el procesamiento de imágenes y diferentes cálculos
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
# Se define el dispositivo de captura de video, en este caso utilizo la webcam del portatil en forma local, pero en vez de eso se puede utilizar una ip de una cámara IP
cam = cv.VideoCapture(0)
# Bucle principal del programa
while(True):
    # Se define la lectura de las imagenes recibidas de la cámara en la variable cam almacenando esto en la variable frame, esto se define dentro del bucle para procesar constantemente cada fotograma capturado
    ret, frame = cam.read()
    # Se definen la altura y anchura a la que queremos cambiar la imagen recibida y la reescalamos definiendo denuevo frame con la función resize
    HW = (640,480)
    frame = cv.resize(frame,HW, interpolation= cv.INTER_LINEAR)
    image_copy = np.array(frame)
    # Se aplican los filtros, gris para eliminar todos los colores de la imágen y canny para mostrar los límites de la imagen recibida para ser procesados más tarde.
    #   Estos límites serán los que nos permitan detectar las diferentes areas y representarlas
    #       Además de aplical este filtro, se ensancha el límite y se le dan bordes rectos con "dilate" y "erode"
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 10,150)
    canny = cv.dilate(canny, None, iterations=1)
    canny = cv.erode(canny, None, iterations=1)
    # Se define cnts (contornos) para que con la función "findContours" defina los contornos de la imagen procesada por los filtros
    cnts,_ = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Se define una lista vacía donde más tarde almacenaremos las areas
    lista_areas = []
    #Segundo bucle el cual realizará iteraciones para cada contorno que encuentre
    for c in cnts:
        # En este bucle se definen las difetentes areas, que serán todos los contornos que se encuentren y entonces se almacenan estas areas en la lista area
        area = cv.contourArea(c)
        lista_areas.append(area)


    # Se define "mas_grande" como el area de mayor valor dentro de la lista, se hace indexando/organizando el contenido dentro de la lista y seleccionando entonces la de mayor valor
        # Conoce el mayor valor porque cada area se define como cuatro puntos en la imagen, los cuatro puntos que formen el cuadrilatero de mayor area serán el area mayor
    mas_grande = cnts[lista_areas.index(max(lista_areas))]
    # Entonces ahora se representa el area mayor y la representamos en la ventana "Calculo de Area y reconocimiento de imagen"
    area = cv.contourArea(mas_grande)
    x,y,w,h = cv.boundingRect(mas_grande)
    cv.rectangle(image_copy, (x,y), (x+w, y+h), (0,255,0), 2)
    cv.imshow('Calculo de Area y Reconocimiento de imagen', image_copy)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()
