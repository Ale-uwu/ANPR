import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#cam = cv.VideoCapture(0)
cam = cv.VideoCapture("https://192.168.0.184:8080/video")
while(True):

    ret, frame = cam.read()
    HW = (640,480)
    frame = cv.resize(frame,HW, interpolation= cv.INTER_LINEAR)
    image_copy = np.array(frame)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 10,150)
    canny = cv.dilate(canny, None, iterations=1)
    canny = cv.erode(canny, None, iterations=1)
    cnts,_ = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    screenCnt = None

#Buscas el contorno más grande
    lista_areas = []
    for c in cnts:
        epsilon = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c,0.018*epsilon,True)
        area = cv.contourArea(c)
        lista_areas.append(area)

#Te quedas con el area más grande
    mas_grande = cnts[lista_areas.index(max(lista_areas))]
#Representas el contorno más grande
    
    area = cv.contourArea(mas_grande)
    x,y,w,h = cv.boundingRect(mas_grande)
    x_mid = int(x+ w/3)
    y_mid = int(y+ h/1.5)
    coords = (x_mid,y_mid)
    color = (0,0,0)
    font = cv.FONT_HERSHEY_DUPLEX
    cv.putText(image_copy,"Cuadrilatero",coords,font,1,color,)
    cv.rectangle(image_copy, (x,y), (x+w, y+h), (255,0,255), 3)

    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv.bitwise_and(frame,frame,mask=mask)
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    text = pytesseract.image_to_string(frame, config='--psm 11')
    print("programming_fever's License Plate Recognition\n")
    print("Detected license plate Number is:",text)
    cv.imshow('Calculo de Area y Reconocimiento de imagen', image_copy)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()