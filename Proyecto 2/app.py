import exifread
import folium
import os
import webbrowser

def get_coordenadas(image_ruta):
    """Extraer las coordenadas GPS de una imagen"""
    with open(image_ruta, 'rb') as image_file:
        tags = exifread.process_file(image_file)

        # Obtener datos GPS
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

        #Verifica si no hay datos de GPS
        if not all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
            return None  # No hay datos GPS

        #Convertir coordenadas a formato decimal
        def convertir_a_decimal(coords, ref):
            degrees, minutes, seconds = [float(x.num) / float(x.den) for x in coords.values]
            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
            if ref in ['S', 'W']:
                decimal = -decimal
            return decimal

        latitude = convertir_a_decimal(gps_latitude, gps_latitude_ref.values[0])
        longitude = convertir_a_decimal(gps_longitude, gps_longitude_ref.values[0])
        return latitude, longitude

def process_images(folder_ruta):
    """Procesar todas las imágenes en una carpeta y obtener sus coordenadas GPS"""
    coordenadas = []
    for file_name in os.listdir(folder_ruta): #Busca archivos en el folder y va agarrando un archivo por un archivo que se encuentre dentro del folder
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):  #Formatos válidos
            image_ruta = os.path.join(folder_ruta, file_name)
            coords = get_coordenadas(image_ruta) #Aqui llama la funcion get_coordenadas para obtener las coordenadas de cada imagen
            if coords:
                coordenadas.append((file_name, coords))  #Guardar nombre y coordenadas
            else:
                print(f"No se encontraron datos GPS en: {file_name}")
    return coordenadas

def crear_mapa(coordenadas, output_file="mapa.html"):
    """Crear un mapa con marcadores para todas las coordenadas"""
    if not coordenadas: #Verifica si no hay coordenadas
        print("No se encontraron coordenadas para generar el mapa.")
        return

    #Centrar el mapa en la primera coordenada
    primera_localizacion = coordenadas[0][1]
    print(primera_localizacion)
    mapa = folium.Map(location=primera_localizacion, zoom_start=10)

    #Añadir marcadores
    for name, (latitude, longitude) in coordenadas: #De coordenadas saca el nombre, latitude y longitude de cada imagen que se guardo en coordenadas
        folium.Marker(
            [latitude, longitude],
            popup=name,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(mapa)

    #Guardar el mapa
    mapa.save(output_file)
    print(f"Mapa guardado como '{output_file}'.")

#Ruta de la carpeta con imágenes
folder_ruta = "imagen/"

#Procesar imágenes y generar el mapa
coordenadas = process_images(folder_ruta)
if coordenadas:
    crear_mapa(coordenadas)
    print("Mapa generado con exito")
    html_file = "mapa.html"
    html_ruta = os.path.abspath(html_file)#Saca la ruta del archivo
    webbrowser.open(f"file://{html_ruta}")#Abre el archivo en el navegador predeterminado
else:
    print("No se encontraron coordenadas GPS en ninguna imagen")
