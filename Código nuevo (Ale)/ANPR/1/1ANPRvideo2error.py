#Se importan las librerias a utilizar en el programa
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Se declara el dispositivo de video (cámara IP) que vamos a usar para el reconocimiento de matrículas
cam = cv2.VideoCapture('http://192.168.18.4:8080/video')
#cam = cv2.VideoCapture(0)

def empty(a):
    pass
cv2.namedWindow("Parametros")
cv2.resizeWindow("Parametros",640,240)
cv2.createTrackbar("threshold1","Parametros",150,250,empty)
cv2.createTrackbar("threshold2","Parametros",150,250,empty)

while(True):    
    ret,frame = cam.read()
    cam_gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    """El motivo del filtro anterior es para marcar limites de figuras
       Estos límites serán reconocidos por "la función findcontours"""

    threshold1 = cv2.getTrackbarPos("threshold1", "Parametros")
    threshold2 = cv2.getTrackbarPos("threshold2", "Parametros")
    canny = cv2.Canny(cam_gris,threshold1,threshold2)

    #for i, contorno in enumerate(contorno):
    #    if i == 0:
    #        continue
    #Estas dos lineas se dedican a aproximar las imperfecciones de la figura-------------------------

    """Epsilon sirve para especificar la precisión de la función de aproximación de la figura
            La variable "True" dentro de epsilon sirve para declarar que es una figura cerrada"""

    #    epsilon = 0.01*cv2.arcLength(contorno, True)

    """Esta es la función que se dedica a aproximar la figura, utilizando epsilon como precisión
            y de nuevo "True" se utiliza para declarar la figura que detecta como una cerrada"""

    #   approx = cv2.approxPolyDP(contorno, epsilon, True)
    #------------------------------------------------------------------------------------------------    
    """Con la función "drawContours" le pedimos al programa que dibuje los contornos de la que detecte,
            en nuestro caso un rectangulo significando las variables lo siguiente:"""
            #Las dos primeras variables nos dan igual ya que nos referimos a la camara y a los contornos
            #El primer 0 se refiere al ID del contorno
            #Los números entre parentesis son el color de dibujado
            #La última veriable representa el grosor del borde
    #    cv2.drawContours(frame, contorno, 0, (0,0,255), 3)

    #    x, y, w, h = cv2.boundingRect(approx)
    #    x_mid = int(x + w/3)
    #    y_mid = int(y + h/1.5)

    #    coordenadas = (x_mid, y_mid)
    #    color = (0,0,0)
    #    font = cv2.FONT_HERSHEY_DUPLEX

    #   if len(approx) == 4:
    #        cv2.putText(frame,"Cuadrilatero",coordenadas, font, 1, color, 1)
        
    cv2.imshow("a",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cam.release()
    cv2.destroyAllWindows()



