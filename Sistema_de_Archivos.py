import zipfile
import os
import Funciones_de_Gmail
#Descomprime archivo, y los guarda

def Descomprimir_Zips()->None:
    informacion_total2 = Funciones_de_Gmail.traer_informacion()
    ruta_zip = "C:\Evaluaciones"
    ruta_extraccion = "C:\Evaluaciones"
    password = None

    for j in informacion_total2:
            print(j)
            mimeMessage = informacion_total2[j][2]

    archivo_zip = zipfile.ZipFile(ruta_zip, "r")
    try:
        print(archivo_zip.namelist())
        archivo_zip.extractall(pwd=password, path=ruta_extraccion)
    except:
        print("ERROR")

    archivo_zip.close()
    create_directory()
    search_local_folders()


def create_directory():
    # Se define el nombre de la carpeta o directorio a crear
    directorio = "C:\Evaluaciones\Docentes\Alumnos"

    try:
        os.mkdir(directorio)

    except OSError:

        print("La creación del directorio %s falló" % directorio)
    else:
        print("Se ha creado el directorio: %s " % directorio)

def search_local_folders()->None:
    list_folders = ["C:\Evaluaciones"]
    directory = "C:\Evaluaciones"
    
    search = input ("\nDesea ingresar a alguna carpeta?(si/no):")

    if search =="si": start =True

    else: start = False
  
    while start:
        Folder = input("\nIngrese el nombre de la carpeta:")
        results = directory + f'\\{Folder}'
    
        if os.path.isdir (results) : #REVISAMOS QUE EL ARCHIVO SEA UNA CAREPTA
            directory = directory +  f'\\{Folder}'
            listing_files = os.listdir(directory) 
            print(f"------------Archivos encoentrados------------")
            list_folders.append(Folder)
            print (listing_files)
        else: 
            print("\nError carpeta incorrecta / inexsistente")

        
        continue_search = input ("\nQuieres seguir buscando (si/no)?" )

        if continue_search != "si": start = False
            
        

