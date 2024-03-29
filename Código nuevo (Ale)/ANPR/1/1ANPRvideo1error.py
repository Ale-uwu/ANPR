# Importar librerias cv2 imutils numpy numpy pytesseract 
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Definir el objeto de captura de imagen (En este caso camara IP) mediante cap (caputure)
    #vid = cv2.VideoCapture(0)
    #camera = cv2.VideoCapture("192.168.18.7:8080/video")
cap = cv2.VideoCapture('http://192.168.18.4:8080/video')

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    conasdtours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in contours:
    
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    
        if len(approx) == 4:
            screenCnt = approx
            break
    if screenCnt is None:
        detected = 0
        print ("No contour detected")

    else:
     detected = 1

    if detected == 1:
        cv2.drawContours(frame, [screenCnt], -1, (0, 0, 255), 3) 

    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv2.bitwise_and(frame,frame,mask=mask)
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    print("License Plate Recognition\n")
    print("Detected license plate Number is:",text)
    if text== "":
        break
    cv2.imshow('video gray', gray)
    cv2.imshow('video original', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
cap.release()
cv2.destroyAllWindows()

