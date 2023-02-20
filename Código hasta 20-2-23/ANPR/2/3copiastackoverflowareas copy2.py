import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

image = cv.imread("caja2.jpg")
image_copy = np.array(image)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

canny = cv.Canny(gray, 10,150)
canny = cv.dilate(canny, None, iterations=1)
canny = cv.erode(canny, None, iterations=1)
cnts,_ = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


#Buscas el contorno más grande
lista_areas = []
for c in cnts:
    area = cv.contourArea(c)
    lista_areas.append(area)


#Te quedas con el area más grande
mas_grande = cnts[lista_areas.index(max(lista_areas))]

#Representas el contorno más grande
area = cv.contourArea(mas_grande)
x,y,w,h = cv.boundingRect(mas_grande)
cv.rectangle(image_copy, (x,y), (x+w, y+h), (0,255,0), 2)
cv.imshow('Calculo de Area y Reconocimiento de imagen', image_copy)
cv.waitKey(0)