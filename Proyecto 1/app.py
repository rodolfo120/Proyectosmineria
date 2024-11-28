import cv2 #Para leer y procesar imagenes
import pytesseract #Para el reconocimiento optico de caracteres
from flask import Flask, render_template

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Define la ruta donde esta instalado el ejecutable de Tesseract OCR
custom_config = r'--oem 3 --psm 6' #Configuracion de Tesseract
#Donde --oem 3 utiliza el modelo OCR LSTM (Long Short-Term Memory), que es el mas preciso
#--psm 6 es el modo de segmentacion de pagina, util para bloques de texto

ruta_imagen = "texto.jpg" #Ruta de la imagen
img = cv2.imread(ruta_imagen) #Se carga en memoria usando opencv

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convierte la imagen a escala de grises

_, binarizacion_img = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY) #Aplica un umbral binario: los píxeles con intensidad mayor o igual a 127 se convierten en blanco (255), y el resto en negro (0). Esto mejora la legibilidad para el OCR.

cv2.imwrite('imagen_procesada.jpg', binarizacion_img) #Se guarda la imagen ya procesada

texto_extraido = pytesseract.image_to_string(binarizacion_img, lang='spa') #Aqui se extrae el texto de la imagen especificando el idioma español

"""De aqui para abajo es para crear una pagina web con flask y visualizar los datos que se extraen de la imagen"""
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', text=texto_extraido)

if __name__ == '__main__':
    app.run(debug=True)