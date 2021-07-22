import service__drive
import pickle
import os
from pathlib import Path 
import io
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd 

def borrar_pantalla()->None:
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

def create_remote_folder(folder_name:str)->None:

    '''
    Pre: Pide ingresar el nombre de la carpeta 
    Post: Crea una carpeteta en tu nube 
    '''
    response=service__drive.obtener_servicio() #LLAMO AL SERVICE PARA PODER IMPORTAR LAS CREDENCIALES
    file_metadata = {'name': folder_name,'mimeType': 'application/vnd.google-apps.folder'} 

    file = response.files().create(body=file_metadata,fields='id').execute() #CREO LA CAREPTA

def create_main_folder()->None:
    '''
    Pre: -
    Post: Crea la carpeta principal del usuario en caso de no encontrarse 
    '''
    directory="C:\\Evaluaciones"
    try:
        os.mkdir(directory)

    except OSError:
        print("")
    else:
        print(f"\nSe creo la carpeta evaluaciones en la direccion C:\\Evaluaciones\n ")

#ASUMO LA HIPOTESIS DE QUE AL DECIR "SE DEBERA REFLEJAR EN EL DRIVE Y EN LOCAL"
#SE REFIERE A CREAR LAS DOS CARPETAS AL MISMO TIEMPO 
def create_local_and_remote_folders()->None:
    '''
    Pre: -
    Post: Crea una carpeta en la nube y en el directorio principal 
    '''
    start = True
    while start:
        folder_name = input ("Ingrese el nombre de la carpeta:")

        create_remote_folder(folder_name) #CREO LA CARPETA EN DRIVE Y TAMBIEN EN LOCAL
        directory=f"C:\\Evaluaciones\\{folder_name}"
        try:
            os.mkdir(directory)

        except OSError:
            print("")
        else:
            print(f"\nCarpeta {folder_name} creada con exito\n ")

        keep_creating = input ("Desea crear otra carpeta?(si/no):")

        if keep_creating != "si": start = False

def dowload_files(diccionary_files:dict)->None:
    '''
    Pre: Pide el ingreso de datos
    Post: Descarga el archivo que seleccione el usuario 
    '''
    diccionary_files={}
    diccionary_files = show_remote_folders_and_files()
    service = service__drive.obtener_servicio() 

    done= True
    while done:
        search_folders(diccionary_files)
        file_to_download = input ("Ingrese el nombre del archivo que quiere descargar:")
        file_name = f'{file_to_download}'

        if file_name in diccionary_files.keys() :
            file_name = diccionary_files[file_name]
            file_id = file_name

            file_name = [f'{file_to_download}']
            file_id = [f'{file_id}']

            for file_id, file_name in zip(file_id,file_name):
                request = service.files().get_media(fileId = file_id)
                fh = io.BytesIO()
                dowloader = MediaIoBaseDownload(fd=fh , request = request)
                start = False
            
                while not start:
                    status, start = dowloader.next_chunk()
                    print("Descargar en proceso  {0}".format(status.progress() * 100)  )
                
                create_main_folder() #EN EL CASO DE QUE NUNCA SE HAYA CREADO UNA CARPETA PRINCIPAL, LA CREAMOS
                fh.seek(0)
                with open (os.path.join ('C:\\Evaluaciones',file_name), 'wb' ) as f:
                    f.write(fh.read())
                    f.close()

        else: print("Ese archivo no existe")

        continue_dowload = input ("Quiere descargar otro archivo (si/no)?:")

        if continue_dowload != "si":
            done = False
'''
def upload_files()->None:
    
    Pre: Pide selecioonar un archivo
    Post: Sube el archivo a google drive
    

    file_metadata = {'name': 'photo.jpg'}
    media = MediaFileUpload(f'C:/Evaluaciones/{file_upload}', mimetype='image/jpeg')
    service = service__drive.obtener_servicio()

    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print ('File ID: %s' % file.get('id'))
'''
def show_remote_folders_and_files()->dict:
    '''
    Pre: -
    Post: Muestra todas las carpetas/archivos que se encuentren en tu google drive
    '''
    diccionary={}

    service=service__drive.obtener_servicio()
    driveid = service.files().get(fileId='root').execute()['id'] #para obtener el drive id y poder listar solo "my-drive"
    
    folder_id=f'{driveid}'
    query=f"parents='{folder_id}' "
    
    response=service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken=response.get('nextPageToken')

    while nextPageToken:
        response=service.files(),list(q=query).execute()
        files.extend(response.get('nextPageToken'))
        nextPageToken=response.get('nextPageToken')


    change_format(files)

    diccionary=folders_and_archives(response,diccionary)
    
    return diccionary

def folders_and_archives(response:None,dictionary:dict)->dict:
    '''
    Pre: -
    Post: Llena un diccionario con las carpetas/archivos de google drive
    '''

    for file in response.get('files'): 
        name=file.get('name')
        id=file.get('id')  

        if id not in dictionary:
            dictionary.update({name:id}) #EN EL CASO DE QUE EL DIC NO CONTENGA LOS ARCHIVOS LE HACEMOS UN UPDATE

    return dictionary

def search_folders(diccionary_folders:dict)->None:
    '''
    Pre: Pide el ingreso de datos
    Post: Revisa si la carpeta ingresada existe y muestra sus datos
    '''
    service=service__drive.obtener_servicio()
    continue_search=input("Quiere buscar en una carpeta?(si/no):")

    if continue_search=="si":
        start=True

    else: 
        start=False

    while start:
        name_folder=input("Escriba el nombre de la carpeta que desea ver:")

        if name_folder in diccionary_folders.keys():            
            name_folder = diccionary_folders[name_folder]
            folder_id = f'{name_folder}'
            query = f"parents='{name_folder}'"

            response=service.files().list(q=query).execute()
            files = response.get('files')
            nextPageToken=response.get('nextPageToken')
            diccionary_folders = folders_and_archives(response,diccionary_folders)
            
            while nextPageToken:
                response = service.files(),list(q=query).execute()
                files.extend(response.get('nextPageToken'))
                nextPageToken = response.get('nextPageToken')
            change_format(files)

        elif name_folder not in diccionary_folders.values():
            print("Esa carpeta no existe")

        continue_search=input("Quiere buscar otra carpeta?(si/no):")
        
        if continue_search=="si" and name_folder in diccionary_folders.values():
            diccionary_folders = folders_and_archives(response,diccionary_folders) #LE SUMAMOS LOS ARCHIVOS AL DIC EN CADA INTERACCION

        elif continue_search!="si":
            start=False
        
def change_format(files)->None:
    '''
    Pre: -
    Post: Cambia el output
    '''
    pd.set_option('display.max_columns',200)
    pd.set_option('display.max_rows',600)
    pd.set_option('display.min_rows',600)
    pd.set_option('display.max_colwidth',200)
    pd.set_option('display.width',200)
    pd.set_option('expand_frame_repr',True)
    df = pd.DataFrame(files)
    print(df)

def show_local_folders_and_files()->None:
    '''
    Pre:-
    Post: Muestra los archivos en la carpeta principal del usuario
    '''
    directory="C:\\Evaluaciones"
    
    if os.path.isdir('C:\\Evaluaciones'):
        listing_files=os.listdir(directory)
        change_format(listing_files)
    
    else:
        create_main_folder()

def search_local_files()->None:
    '''
    Pre: Pide datos de una carpeta
    Post: Se mueve sobre esa carpeta y muestra sus datos
    '''
    directory="C:\\Evaluaciones"
    search= input ("\nDesea realizar una busqueda (si/no)?" )

    #while search != "no":
        #name_file = input ("\nEscriba el nombre de la carpeta que desea buscar:")        
        #search = input ("Escriba no para salir:") #POR AHORA SOLO SE PUEDEN VER LOS ARCHIVOS EN LA CARPETA PRINCIPAL

def file_list_menu()->None:
    '''
    Pre: -
    Post: Muestra las opciones disponibles sobre 
    '''
    print("-------OPCIONES------")
    print("1-Ver archivos en Google Drive")
    print("2-Ver archivos descargados")
    print("")
    opcion=validar_rango()

    if opcion == 1:
        borrar_pantalla()
        diccionary = {}
        print("---------Archivos que se encuentran en tu cuenta de gogle drive---------")
        diccionary = show_remote_folders_and_files()
        search_folders(diccionary)

    elif opcion==2:
        print("---------Archivos que se encuentran en tu carpeta principal---------")
        show_local_folders_and_files()
        search_local_files()
        print("")

def dowload_menu()->None:
    print("-------OPCIONES------")
    print("1-Descargar archivos")
    print("2-Salir")
    #print("2-Descargar carpetas")
    print("")
    opcion=validar_rango()

    if opcion == 1:
        diccionary_files = {}
        dowload_files(diccionary_files)

    #elif opcion == 2:
        

def menu_create_archives():
    print("-------OPCIONES------")
    #print("1-Crear una archivo")
    print("1-Crear una carpeta")
    print("2-Salir")
    #print("2-Crear un archvio")
    opcion=validar_rango()

    if opcion == 1:
        create_local_and_remote_folders()

    #elif opcion == 2:
        