import cv2
import pytesseract
from flask import Flask, render_template

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 6'

ruta_imagen = "imagen.jpg"
img = cv2.imread(ruta_imagen)

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, binarizacion_img = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite('imagen_procesada.jpg', binarizacion_img)

texto_extraido = pytesseract.image_to_string(binarizacion_img, lang='spa')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', text=texto_extraido)

if __name__ == '__main__':
    app.run(debug=True)