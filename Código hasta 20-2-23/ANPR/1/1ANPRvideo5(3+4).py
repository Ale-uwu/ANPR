#Se importan las librerias a utilizar en el programa, las que vamos a utilizar mas importantes son: cv2 (opencv y pytessereact, el OCR)
import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#==========================================================================================================================================
# La definición de nada se utilizará un poco más adelante para los deslizadores del filtro "treshold" el cual se utilizará para delimitar las imágenes en lineas simples, esto con el objetivo de detectar cuadrilateros en las imágenes
def nada(x):
    pass
#Se declara el dispositivo de video (cámara IP) que vamos a usar para el reconocimiento de matrículas
#cam = cv2.VideoCapture('http://192.168.18.4:8080/video') 
#cam = cv2.VideoCapture("http://192.168.251.107:8080/video") 
cam = cv2.VideoCapture(0)
#--------------------------------------------------------------------------     
# Se crea la ventana llamada "a" (podría ser cualquier nombre), en esta ventana, al ejecutar el programa se encontrarán las barras deslizadores del filtro Treshold y la imagen con el filtro aplicado
cv2.namedWindow("a")
cv2.createTrackbar("lim1","a",0,255,nada)
cv2.createTrackbar("lim2","a",0,255,nada)
#225, 250 optimos
#--------------------------------------------------------------------------   
# Bucle principal del programa, me iré parando en deferentes partes
while(True):    
    #== Se lee la imágen que nos envía la camara a través de "cam" y lo definimos en "frame" esto se hace dentro del bucle para que se procese cada fotograma uno tras otro
    # HW lo utilizo para redimensionar la imagen y que no la envie con tanta resolución esto además es para hacer las ventanas más pequeñas
    ret, frame = cam.read()
    HW = (640,480)
    frame = cv2.resize(frame,HW, interpolation= cv2.INTER_LINEAR)
    image_copy = np.array(frame)
    #===================================================================
    # Se aplican los diferentes filtros:
    #   - Gris: Para eliminar colores y que el filtro treshold no detecte más contornos de los que debe
    #   - Límite: Filtro canny para detectar los contornos, además de aplicar el simple filtro hacemos que los contornos se hagan mas anchos con "dilate" y tengan bordes cuadrados con "erode"
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    L1 = cv2.getTrackbarPos("lim1","a")
    L2 = cv2.getTrackbarPos("lim2","a")
    limite = cv2.Canny(gris,L1,L2,cv2.THRESH_BINARY)
    limite = cv2.dilate(limite, None, iterations=1)
    limite = cv2.erode(limite, None, iterations=1)
    ##contornos, jerarquia = cv2.findContours(limite,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # Para detectarlos contornos se guardan estos en la variable "contornos" y se buscan dentro de la variable límite
    contornos, jerarquia = cv2.findContours(limite,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # El segundo bucle sirve para enumerar los contornos para más tarde representar esta cantidad
    for i, contornos in enumerate(contornos):
        if i == 0:
            continue
        # Las dos siguientes variables son números utilizados para aproximar los contornos detectados a cuadrilateros
        epsilon  = 0.018*cv2.arcLength(contornos,True)
        approx = cv2.approxPolyDP(contornos, epsilon,True)
        # ahora se representan los contornos encontrados en la ventada frame "imagen sin filtros"
        cv2.drawContours(frame, contornos, 0, (0,0,255), 3)
        #aquí se definen las coordenadas en las que se representan los cuadrilateros utilizando approx para dibujar un rectangulo aproximado de la imagen obtenida
        x, y, w, h = cv2.boundingRect(approx)
        x_mid = int(x + w/3)
        y_mid = int(y + h/1.5)
        # se definen las coordenadas donde va a ir el texto
        coordenadas = (x_mid, y_mid)
        color = (0,0,0)
        font = cv2.FONT_HERSHEY_DUPLEX

        if len(approx) == 4:
            cv2.putText(frame,"Cuadrilatero",coordenadas, font, 1, color, 1)
    # Se crean el resto de las ventanas donde se va a ver la imagen de la cámara con los distintos filtros
    cv2.imshow('Calculo de Area y Reconocimiento de imagen', image_copy)
    cv2.imshow("b",frame)
    cv2.imshow("c",gris)
    cv2.imshow("a",limite)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()



