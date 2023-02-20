#Se importan las librerias a utilizar en el programa
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def nada(x):
    pass

#Se declara el dispositivo de video (cámara IP) que vamos a usar para el reconocimiento de matrículas
cam = cv2.VideoCapture('http://192.168.18.4:8080/video')
#--------------------------------------------------------------------------     
cv2.namedWindow("a")
cv2.createTrackbar("lim1","a",0,255,nada)
cv2.createTrackbar("lim2","a",0,255,nada)
#225, 250 optimos
#--------------------------------------------------------------------------    

while(True):    

    ret, frame = cam.read()
    HW = (640,480)
    frame = cv2.resize(frame,HW, interpolation= cv2.INTER_LINEAR)
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    L1 = cv2.getTrackbarPos("lim1","a")
    L2 = cv2.getTrackbarPos("lim2","a")
    limite = cv2.Canny(gris,L1,L2)
    contornos, jerarquia = cv2.findContours(limite,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    #cv2.imshow("a",frame)
    #cv2.imshow("a",gris)
    cv2.imshow("a",limite)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()



