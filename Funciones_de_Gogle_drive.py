import service__drive
import os
import io
from googleapiclient.http import MediaFileUpload


def borrar_pantalla():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def validar_rango() -> int:
    '''
    Pre: Pide un numero en un rango
    Post: Te responde si el numero esta en el rango
    '''
    opcion = input("Ingrese una opcion: ")                        
    while not opcion.isnumeric()  or (int(opcion)) >2 or (int(opcion)) <1 :
        print("")
        print("Esa opcion no es valida!")
        print("")
        opcion = input("Ingrese una opcion valida:")

    return int(opcion)



def mostrar_archivos()->None:
    '''
    Pre: -
    Post: Muestra las carpetas en tu cuenta de google drive
    '''
    comenzar=True
    page_token = None
    resultados=[]
    nombre=""
    query="mimeType ='application/vnd.google-apps.folder'" #PARA QUE SOLAMENTE FILTRE LAS CARPETAS

    while comenzar:
        response=service__drive.obtener_servicio()
        results=response.files().list(q=query ,spaces='drive',fields='nextPageToken, files(id, name)',pageToken=page_token).execute()
    
        for file in results.get('files'):     
            print(f" Nombre del archivo: {file.get('name')}, ID:{file.get('id')}") 
            page_token = results.get('nextPageToken', None)
            
            
                

            if page_token is None:
                comenzar=False

def listar_archivos():
    print("-------OPCIONES------")
    print("1-Ver archivos en Google Drive")
    print("2-Ver archivos descargados")
    print("")
    opcion=validar_rango()

    if opcion==1:
        borrar_pantalla()
        print("---------Archivos que se encuentran en tu cuenta de gogle drive---------")
        mostrar_archivos()
        print("")

    elif opcion==2:
        print("")


