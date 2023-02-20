#Se importan las librerias a utilizar en el programa
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def nada(x):
    pass

#Se declara el dispositivo de video (cámara IP) que vamos a usar para el reconocimiento de matrículas
#cam = cv2.VideoCapture('http://192.168.18.4:8080/video')
cam = cv2.VideoCapture("http://192.168.123.189:8080/video")  

while(True):    

    ret, frame = cam.read()
    HW = (640,480)
    frame = cv2.resize(frame,HW, interpolation= cv2.INTER_LINEAR)
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    limite = cv2.Canny(gris,225,250,cv2.THRESH_BINARY)
    contornos, jerarquia = cv2.findContours(limite,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for i, contornos in enumerate(contornos):
        if i == 0:
            continue
        epsilon  = 0.01*cv2.arcLength(contornos,True)
        approx = cv2.approxPolyDP(contornos, epsilon,True)

        cv2.drawContours(frame, contornos, 0, (0,0,255), 3)
    
        x, y, w, h = cv2.boundingRect(approx)
        x_mid = int(x + w/3)
        y_mid = int(y + h/1.5)

        coordenadas = (x_mid, y_mid)
        color = (0,0,0)
        font = cv2.FONT_HERSHEY_DUPLEX

        if len(approx) == 4:
            cv2.putText(frame,"Cuadrilatero",coordenadas, font, 1, color, 1)


    cv2.imshow("a",frame)
    #cv2.imshow("a",gris)
    cv2.imshow("a",limite)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()



