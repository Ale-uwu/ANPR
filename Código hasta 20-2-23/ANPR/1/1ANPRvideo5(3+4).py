#Se importan las librerias a utilizar en el programa
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 
c = 0
def nada(x):
    pass
#Se declara el dispositivo de video (cámara IP) que vamos a usar para el reconocimiento de matrículas
#cam = cv2.VideoCapture('http://192.168.18.4:8080/video') 
#cam = cv2.VideoCapture("http://192.168.251.107:8080/video") 
cam = cv2.VideoCapture(0)
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
    image_copy = np.array(frame)
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    L1 = cv2.getTrackbarPos("lim1","a")
    L2 = cv2.getTrackbarPos("lim2","a")
    limite = cv2.Canny(gris,L1,L2,cv2.THRESH_BINARY)
    limite = cv2.dilate(limite, None, iterations=1)
    limite = cv2.erode(limite, None, iterations=1)
    ##contornos, jerarquia = cv2.findContours(limite,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contornos, jerarquia = cv2.findContours(limite,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    lista_areas = []
    for i, contornos in enumerate(contornos):
        if i == 0:
            continue
        mas_grande = contornos[lista_areas.index(max(lista_areas))]
        epsilon  = 0.018*cv2.arcLength(contornos,True)
        approx = cv2.approxPolyDP(contornos, epsilon,True)
        area = cv2.contourArea(mas_grande)
        s,d,f,g = cv2.boundingRect(mas_grande)
        cv2.rectangle(image_copy, (s,d), (s+f, d+g), (0,255,0), 2)


        cv2.drawContours(frame, contornos, 0, (0,0,255), 3)
        x, y, w, h = cv2.boundingRect(approx)
        x_mid = int(x + w/3)
        y_mid = int(y + h/1.5)

        coordenadas = (x_mid, y_mid)
        color = (0,0,0)
        font = cv2.FONT_HERSHEY_DUPLEX

        if len(approx) == 4:
            cv2.putText(frame,"Cuadrilatero",coordenadas, font, 1, color, 1)

    cv2.imshow('Calculo de Area y Reconocimiento de imagen', image_copy)
    cv2.imshow("b",frame)
    cv2.imshow("c",gris)
    cv2.imshow("a",limite)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()



