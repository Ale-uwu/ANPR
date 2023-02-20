import cv2
import numpy as np
import xlsxwriter

def SkinColorUpper (Hue,mult1,mult2):
    upper = [Hue,mult1*255,mult2*255]
    upper = np.array(upper)
    return upper

def SkinColorLower (Hue,mult1,mult2):
    lower = [Hue,mult1*255,mult2*255]
    lower = np.array(lower)
    return lower

#cam = cv2.VideoCapture(0)
#ret, img = cam.read()
img = cv2.imread('E:\\vscode\\.vscode\\ANPR\\imagenes\\matricula.jpg',cv2.IMREAD_COLOR)
# cv2.imshow("Imagen",img)
# cv2.waitKey(0)
heigth, width = img.shape[:2]
#print (img.shape)

start_row,start_col = int(0),int(0)
end_row, end_col = int(heigth), int(width*.3)
img = img[start_row:end_row,start_col:end_col]

hls = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)

mask = cv2.inRange(hls,SkinColorLower(0,0.2,0),SkinColorUpper(27,0.72,0.75))
#mask = cv2.inRange(hls,np.array([0,49,61]),np.array([20,255,127]))

blur = cv2.medianBlur(mask,5)

ret,edges = cv2.threshold(blur,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_CHRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
edges= cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

contours, hierarchy = cv2.findContours(edges.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
draw = cv2.drawContours(img,contours,-1,(255,0,0),3)
#print(contours)
cv2.imshow("mask",img)
cv2.waitKey(0)

for component in zip(contours,hierarchy):
    current_contour = component[0]
    # cv2.imshow("img_resize",current_contour)
    # cv2.waitKey(0)
    x,y,w,h = cv2.boundingRect(current_contour)
    p = cv2.arcLength(current_contour,True)
    epsilon = p*0.015
    approx = cv2.approxPolyDP(current_contour,epsilon,True)
    lados = len(approx)
    empty = np.zeros((h,w),np.uint8)
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
    roi = edges[y:y+h,x:x+w]
    empty[0:h,0:w]=roi
    edges=empty
    # cv2.imshow("Edges",edges)
    # cv2.waitKey(0)  
    img_resize = cv2.resize(edges,(150,150),interpolation=cv2.INTER_AREA)
    ret, edges_res = cv2.threshold(img_resize,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow("img_resize",img_resize)
    # cv2.waitKey(0)
    contours_2,hierarchy_2 = cv2.findContours(edges_res.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for component_2 in zip(contours_2,hierarchy_2):
        currentContour =  component_2[0]
        x,y,w,h = cv2.boundingRect(currentContour)
        M = cv2.moments(currentContour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        A = cv2.contourArea(currentContour)
        p = cv2.arcLength(currentContour,True)
        aP=A/float(p*p)
        #print(M['m10'],M['m01'],M['m00'],cx,cy,A,p,aP)
        Hu = cv2.HuMoments(M)
        # print(Hu)
cv2.destroyAllWindows()