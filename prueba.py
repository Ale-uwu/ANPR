#include<opencv2\opencv.hpp>
#include<iostream>
 
using namespace cv;
using namespace std;
//Variables Globales
int parametro1 = 30;
int parametro2 = 100;
int parametro3 = 10;
Vec3b pixel;
 
void onMouseV(int event, int x, int y, int flags, void*param);
void onMouse(int event, int x, int y, int flags, void *param);
void mostrarVideo(VideoCapture c, int filtro);
void mostrarFoto(VideoCapture c);
int menu();
 
int main() {
    VideoCapture c;
    int op;
    do {
        op = menu();
        switch (op) {
        case 0: cout << "Adios" << endl;
            break;
        case 1: mostrarFoto(c);
            break;
        case 2: mostrarVideo(c, 0);
            break;
        case 3: mostrarVideo(c, 1);
            break;
        case 4: mostrarVideo(c, 2);
            break;
        case 5: mostrarVideo(c, 3);
            break;
        case 6: mostrarVideo(c, 4);
            break;
        case 7: mostrarVideo(c, 5);
            break;
        case 8: mostrarVideo(c, 6);
            break;
        case 9: mostrarVideo(c, 7);
            break;
        case 10: mostrarVideo(c, 8);
            break;
        case 11: mostrarVideo(c, 9);
            break;
        case 12: mostrarVideo(c, 10);
            break;
        case 13: mostrarVideo(c, 11);
            break;
        case 14: mostrarVideo(c, 12);
            break;
        case 15: mostrarVideo(c, 13);
            break;
        case 16: mostrarVideo(c, 14);
            break;
        case 17:mostrarVideo(c, 15);
            break;
        case 18: mostrarVideo(c, 16);
            break;
        }
    } while (op != 0);
    return 1;
}
 
int menu() {
    int opcion;
    cout << "------Menu------" << endl;
    cout << " 0. Salir" << endl;
    cout << " 1. Foto" << endl;
    cout << " 2. Video" << endl;
    cout << " 3. Deteccion de Bordes" << endl;
    cout << " 4. Distorsion" << endl;
    cout << " 5. Distorsion Gaussiana" << endl;
    cout << " 6. Distorsion Mediana" << endl;
    cout << " 7. Box Filter" << endl;
    cout << " 8. Disminuir Resolucion" << endl; //Desenfoca una imagen y disminuye la resolución de la misma
    cout << " 9. Aumentar Resolucion" << endl;
    cout << "10. Filtro Bilateral" << endl;
    cout << "11. Escala de Grises" << endl;
    cout << "12. Laplacian" << endl;
    cout << "13. Binario" << endl;
    cout << "14. Sobel" << endl;
    cout << "15. Erode" << endl;
    cout << "16. Binario Inverso" << endl;
    cout << "17. Dilate" << endl;
    cout << "18. Filtrado de Colores por Mouse" << endl;
    cout << "Selecciona una opcion: " << endl;
    cin >> opcion;
    return opcion;
}
 
void mostrarFoto(VideoCapture c) {
    c.open(1);
    if (!c.isOpened()) {
        cout << "Error al tratar de inicializar la camara" << endl;
    }
    else {
        namedWindow("Foto", 1);
        moveWindow("Foto", 50, 200);
        Mat frame;
        Mat frameHSV;
        c >> frame;
        c.release();
        flip(frame, frame, 1);
        imshow("Foto", frame);
        cvtColor(frame, frameHSV, COLOR_BGR2HSV);
        setMouseCallback("Foto", onMouse, reinterpret_cast<void*>(&frame));
        waitKey(0);
        destroyWindow("Foto");
    }
}
 
void onMouse(int event, int x, int y, int flags, void *param) {
    VideoCapture c;
    Mat *imagen = reinterpret_cast<Mat*>(param);
    Vec3b pixel;
    switch (event){
 
    case CV_EVENT_LBUTTONDOWN:
        c.open(0);
        destroyWindow("Foto");
        pixel = imagen->at<Vec3b>(y, x);
        cout << "Click en [" << x << "," << y << "] el color es: " << (int)pixel[0] << "," << (int)pixel[1] << "," << (int)pixel[2] << endl;
        namedWindow("Video", 1);
        moveWindow("Video", 700, 200);
        while (true)
        {
            Mat image;
            Mat dilateElement = getStructuringElement(MORPH_RECT, Size(20, 20));
            Mat erodeElement = getStructuringElement(MORPH_RECT, Size(10, 10));
            Mat frameMorph;
            Mat frameHSV;
            Mat frameBlur;
            Mat frameRange;
            c >> image;
            flip(image, image, 1);
            cvtColor(image, frameHSV, COLOR_BGR2HSV);
            //Suavizar los borders, smoothing, blur
            blur(frameHSV, frameBlur, Size(15, 15));
            Scalar minValues = Scalar(pixel[0] - 20, pixel[1] - 30, pixel[2] - 30);
            Scalar maxValues = Scalar(pixel[0] + 20, pixel[1] + 30, pixel[2] + 30);
            inRange(frameBlur, minValues, maxValues, frameRange);
            //Filtros Morfologicos, dilatacion y erosion
            dilate(frameRange, frameMorph, dilateElement, Point(-1, -1), 2);
            erode(frameMorph, frameMorph, erodeElement, Point(-1, -1), 2);
            imshow("Video Filtrado", frameMorph);
            if (waitKey(30) >= 0)
            {
                break;
            }
        }
        destroyAllWindows();
        c.release();
    }
}
 
void onMouseV(int event, int x, int y, int flags, void*param) {
    Mat *imagen = reinterpret_cast<Mat*>(param);
    if (event == CV_EVENT_FLAG_LBUTTON) {
        pixel = imagen->at<Vec3b>(y, x);
        cout << "Click en [" << x << "," << y << "] el color HSV es:" << (int)pixel[0] << "," << (int)pixel[1]
            << "," << (int)pixel[2] << endl;
    }
}
 
// filtro, indica el filtro a aplicar
//0. video original
//1. Canny
//2. Blur
void mostrarVideo(VideoCapture c, int filtro) {
    c.open(1);
    if (!c.isOpened()) {
        cout << "Error al tratar de inicializar la camara" << endl;
    }
    else {
        namedWindow("Video Original", 1);
        moveWindow("Video Original", 50, 200);
        if (filtro != 0) {
            namedWindow("Video Filtrado", 1);
            moveWindow("Video Filtrado", 700, 200);
            createTrackbar("tb1", "Video Original", &parametro1, 255);
            createTrackbar("tb2", "Video Original", &parametro2, 255);
            createTrackbar("tb3", "Video Original", &parametro3, 255);
        }
        while (true) {
            // crea la estructura del elemento
            int erosion_size = 6;
            Mat elemento = getStructuringElement(MORPH_CROSS,Size(2 * erosion_size + 1, 2 * erosion_size + 1),Point(erosion_size, erosion_size));
            int dilatar = 1;
            Mat frame;
            Mat filtrada;
            Mat filtrada1;
            Mat filtrada2;
            Mat dilateElement = getStructuringElement(MORPH_RECT, Size(20, 20));
            Mat erodeElement = getStructuringElement(MORPH_RECT, Size(10, 10));
            Mat frameMorph;
            Mat frameHSV;
            Mat frameBlur;
            Mat frameRange;
            c >> frame;
            flip(frame, frame, 1);
            imshow("Video Original", frame);
            setMouseCallback("Video Original", onMouseV, reinterpret_cast<void*>(&frameHSV));
            switch (filtro) {
            case 1:
                Canny(frame, filtrada, parametro1, parametro2);
                imshow("Video Filtrado", filtrada);
                break;
            case 2:
                parametro1 = (parametro1 > 0) ? parametro1 : 1; // Operador ternario
                blur(frame, filtrada, Size(parametro1, parametro1));
                imshow("Video Filtrado", filtrada);
                break;
            case 3:
                parametro1 = (parametro1 % 2 == 0) ? parametro1 + 1 : parametro1;
                GaussianBlur(frame, filtrada, Size(parametro1, parametro1), parametro3);
                imshow("Video Filtrado", filtrada);
                break;
            case 4:
                parametro1 = (parametro1 % 2 == 0) ? parametro1 + 1 : parametro1;
                parametro1 = (parametro1 > 0) ? parametro1 : 1;
                medianBlur(frame, filtrada, parametro1);
                imshow("Video Filtrado", filtrada);
                break;
            case 5:
                parametro1 = (parametro1 > 0) ? parametro1 : 1;
                boxFilter(frame, filtrada, -1, Size(parametro1, parametro1));
                imshow("Video Filtrado", filtrada);
                break;
            case 6:
                pyrDown(frame, filtrada);
                imshow("Video Filtrado", filtrada);
                break;
            case 7:
                pyrUp(frame, filtrada);
                imshow("Video Filtrado", filtrada);
                break;
            case 8:
                bilateralFilter(frame, filtrada, parametro3, parametro1, parametro2);
                imshow("Video Filtrado", filtrada);
                break;
            case 9:
                cvtColor(frame, filtrada, CV_BGR2GRAY);
                imshow("Video Filtrado", filtrada);
                break;
            case 10:
                cvtColor(frame, filtrada, CV_BGR2GRAY);
                Laplacian(filtrada, filtrada1, CV_16S, 3, 1, 0);
                convertScaleAbs(filtrada1, filtrada2);
                imshow("Video Filtrado", filtrada2);
                break;
            case 11:
                cvtColor(frame, filtrada, CV_BGR2GRAY);
                threshold(filtrada, filtrada1, parametro1, 255, CV_THRESH_BINARY);
                imshow("Video Filtrado", filtrada1);
                break;
            case 12:
                Sobel(frame, filtrada, 0, 1, 0, 3, parametro1, parametro2);
                imshow("Video Filtrado", filtrada);
                break;
            case 13:
                // aplica erocion a la imagen
                erode(frame, filtrada, elemento);  // dilatar(frame,filtrada,element);
                imshow("Video filtrado", filtrada);
                break;
            case 14:
                cvtColor(frame, filtrada, CV_BGR2GRAY);
                threshold(filtrada, filtrada1, parametro1, 255, CV_THRESH_BINARY_INV);
                imshow("Video Filtrado", filtrada1);
                break;
            case 15:
                dilate(frame, filtrada, elemento);
                imshow("Video filtrado", filtrada);
                break;
            case 16:
                cvtColor(frame, frameHSV, COLOR_BGR2HSV);
                //Suavizar los borders, smoothing, blur
                blur(frameHSV, frameBlur, Size(15, 15));
                Scalar minValues = Scalar(pixel[0] - parametro1, pixel[1] - parametro2, pixel[2] - parametro3);
                Scalar maxValues = Scalar(pixel[0] + parametro1, pixel[1] + parametro2, pixel[2] + parametro3);
                inRange(frameBlur, minValues, maxValues, frameRange);
                //Filtros Morfologicos, dilatacion y erosion
                dilate(frameRange, frameMorph, dilateElement, Point(-1, -1), 2);
                erode(frameMorph, frameMorph, erodeElement, Point(-1, -1), 2);
                imshow("Video Filtrado", frameMorph);
                break;
            }
            if (waitKey(30) >= 0) {
                break;
            }
        }
        destroyAllWindows();
    }
}