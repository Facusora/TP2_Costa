import service__drive
import pickle
import os
from pathlib import Path 
import io
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd 
import yaml

def borrar_pantalla()->None:
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def validar_rango(range) -> int:
    '''
    Pre: Pide un numero en un rango
    Post: Te responde si el numero esta en el rango
    '''
    opcion = input("Ingrese una opcion: ")                        
    while not opcion.isnumeric()  or (int(opcion)) >range or (int(opcion)) <1 :
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
#SE REFIERE A CREAR LAS DOS CARPETAS EN REMOTO/LOCAL
def create_local_and_remote_folders()->None:
    '''
    Pre: -
    Post: Crea una carpeta en la nube y en el directorio principal 
    '''
    start = True
    while start:
        folder_name = input ("Ingrese el nombre de la carpeta:")
        create_main_folder() #EN CASO DE QUE LA CARPETA PRINCIPAL NO ESTE CREADA, LA CREO

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
        
def select_extension()->str:
    '''
    Pre: Pide ingresar un formato de archivo
    Post: Valida que el formato este disponible
    '''
    diccionary_extensions = {'Texto':'.txt', 
                            'Word':'.docx',}

    borrar_pantalla()
    print("-------TIPOS DE EXTENSIONES DISPONIBLES-----------")
    for keys in diccionary_extensions:
        print(yaml.dump(keys)) #BIBLIOTECA PARA MEJORAR EL PRINT DEL DICCIONARIO

    start = True
    while start :
        extension = input ("Ingrese el nombre la extension que desea que tenga el archivo:")
        mimetype = select_mymetype(extension)

        if extension in diccionary_extensions.keys():     #PIDO QUE LA EXTENSION ESTE EN EL DIC
            extension = diccionary_extensions[extension]
            start = False
            return extension, mimetype
            
        elif extension not in diccionary_extensions.keys():    #SI LA EXTENSION NO ESTA EN EL DIC QUE SIGA CICLANDO
            print("\nEsa extension no esta disponible\n")


def create_remote_and_local_files()->None:
    '''
    Pre: Pide ingresar un nombre y un formato
    Post: Crea una archivo en la carpeta principal del usuario
    '''
    path = 'C:\Evaluaciones'  #GENERO LOS ARCHIVOS EN LA CARPETA PRINCIPAL DEL USUARIO
    start = True
    while start :
        file_name = input ("\nIngrese el nombre del archivo que quiere crear:")

        if file_name !="":
            
            extension, mimetype = select_extension()
            file_format = file_name + extension
            create_remote_files(file_format, mimetype)
            
            while not os.path.exists(path):
                os.mkdir(path)

            route =f'{path}' + f'\\{file_format}'
            archive = open(route, 'w')
            archive.close()
    
            create_another_file = input ("\nQuieres crear otro archivo?(si/no):")

            if create_another_file !="si": start = False
        
        else :print("\nDebe ingresar un nombre para el archivo")

def create_remote_files(file_name:str,mimeType:str):
    '''
    Pre: -
    Post: Crea un archivo en la nube
    '''
    drive_service = service__drive.obtener_servicio()

    file_metadata = {
    'name' :f'{file_name}',
    'mimeType' :f'{mimeType}'            
    }                     

    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()


def select_mymetype(mimeType:str)->str:
    '''
    Pre: -
    Post: Returna la extension del archivo a crear
    '''
    diccionary_mimeType = {'Texto':'.txt','Word':'application/vnd.google-apps.document',}
    
    if mimeType in diccionary_mimeType.keys():
        mimeType = diccionary_mimeType[mimeType]#PIDO QUE LA EXTENSION ESTE EN EL DIC

    return mimeType

def show_local_folders_and_files()->None:
    '''
    Pre:-
    Post: Muestra los archivos en la carpeta principal del usuario
    '''
    directory="C:\\Evaluaciones"
    
    if os.path.isdir('C:\\Evaluaciones'):
        listing_files=os.listdir(directory)
        print("-----------------Carpeta principal del usuario-----------------")
        change_format(listing_files)
    
    else:
        create_main_folder()

def search_local_folders()->None:
    list_folders = ['C:\Evaluaciones']
    directory = 'C:\Evaluaciones'
    
    search = input ("\nDesea ingresar a alguna carpeta?(si/no):")

    if search =="si": start =True

    else: 
        start = False 
        results = directory
  
    while start:
        Folder = input("\nIngrese el nombre de la carpeta:")
        results = directory + f'\\{Folder}'
    
        if os.path.isdir (results) : #REVISAMOS QUE EL ARCHIVO SEA UNA CAREPTA
            borrar_pantalla()
            directory = directory +  f'\\{Folder}'
            listing_files = os.listdir(directory) 

            print(f"------------Archivos encontrados en la carpeta {Folder}------------")
            change_format(listing_files)
            list_folders.append(Folder)

        else: 
            results = directory
            print("\nError carpeta incorrecta / inexsistente")

        list_folders, directory = back_folders (Folder,list_folders) #LLAMAMOS A LA FUNCION "BACK FOLDERS" PARA PREGUNTAR SI EL USUARIO QUIERE VOLVER ATRAS
        continue_search = input ("\nQuieres seguir buscando (si/no)?" )

        if continue_search != "si": 
            start = False

    return results

def back_folders(Folder:str,list_folders:list):
    start = True
    while start:
        back = input( "\nQuieres volver atras (si/no)?:")

        if back != "si":
            route = '\\'.join(list_folders)
            start = False

        elif back =="si" and len(list_folders)>1 :
            borrar_pantalla()

            list_folders.pop()
            route = '\\'.join(list_folders)
            listing_files = os.listdir(route)
            position = len(list_folders) #USAMOS EL LEN PARA SABER EL LARGO DE LA LISTA Y SABER EN QUE CARPETA ESTAMOS
            print(f"------------Archivos encoentrados {list_folders[position -1 ]}------------")
            change_format(listing_files)

        else :
            route = '\\'.join(list_folders)
            start = False 
            print("\nEstas en el directorio principal") 

    return list_folders, route

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
    
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response=service.files(),list(q=query).execute()
        files.extend(response.get('nextPageToken'))
        nextPageToken=response.get('nextPageToken')

    change_format(files)

    diccionary = folders_and_archives(response,diccionary)
    
    return diccionary

def folders_and_archives(response:None,dictionary:dict)->dict:
    '''
    Pre: -
    Post: Llena un diccionario con las carpetas/archivos de google drive
    '''
    for file in response.get('files'): 
        name = file.get('name')
        id = file.get('id')  

        if id not in dictionary:
            dictionary.update({name:id}) #EN EL CASO DE QUE EL DIC NO CONTENGA LOS ARCHIVOS LE HACEMOS UN UPDATE

    return dictionary

def search_in_remote_folders(diccionary_folders:dict)->None:
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
        borrar_pantalla()
        diccionary_files = show_remote_folders_and_files()
        search_in_remote_folders(diccionary_files)

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
                results = choose_dowload_location() #FUNCION PARA DEFINIR LA LOCACION DONDE EL USUARION QUIERA DESCARGAR 
    
                start = False
                while not start:
                    status, start = dowloader.next_chunk()
                    print("Descargar en proceso  {0}".format(status.progress() * 100)  )
                    create_main_folder() #EN EL CASO DE QUE NUNCA SE HAYA CREADO UNA CARPETA PRINCIPAL, LA CREAMOS

                fh.seek(0)
                with open (os.path.join (f'{results}',file_name), 'wb' ) as f: #MODIFICO PARA PRUEBAS
                    f.write(fh.read())
                    f.close()

        else: print("Ese archivo no existe")

        continue_dowload = input ("Quiere descargar otro archivo (si/no)?:")

        if continue_dowload != "si": done = False

def choose_dowload_location():
    borrar_pantalla()
    print("\nSeleccione la carpeta donde desea descargar el archivo\n")
    show_local_folders_and_files()
    results = search_local_folders()

    return results

def search_folder_upload():
    search_in_folders = input ("Quieres buscar en alguna carpeta?:")

def prepare_to_upload(direction:str,file_name:str):
    '''
    Pre: -
    Post: Sube un archivo a la carpeta principal de google drive
    '''
    service = service__drive.obtener_servicio()
    folder_id = service.files().get(fileId='root').execute()['id']

    file_metadata = {
        "name":f"{file_name}",             
        "parents": [folder_id]
    }
    media = MediaFileUpload(f'{direction}', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
        
def select_file_to_upload()->str:
    start = True
    continue_upload = ""
    show_local_folders_and_files()
    route = search_local_folders()

    while start:    
        file_name = input ("\nIngrese el nombre del archivo que desea subir:")
        direction = route + f'\\{file_name}'
    
        if os.path.isfile (direction) :
            start = False
            print("\nArchivo encontrado, preparando para subir a drive")

        else: 
            print("\nError nombre del archivo incorrecto")
            continue_upload = input ("\nQuiere intentar descargar otro archivo de esta carpeta (si/no)?:")
        
        if continue_upload == "no":
            start = False
            file_name = ""
            direction = ""

        else : print ("")

    return direction, file_name

def upload_files():
    start = True
    while start:
        borrar_pantalla() 
        direction, file_name = select_file_to_upload() #FUNCION PARA BUSCAR EL ARCHIVO QUE DESEA SUBIR EL USUARIO
      
        if direction !="" and file_name !="":
            prepare_to_upload(direction, file_name)
            print("\nArchivo subio con exito")

        continue_upload = input ("\nQuieres subir otro archivo (si/no)?:")

        if continue_upload !="si":
            start = False

def file_list_menu()->None:
    '''
    Pre: -
    Post: Muestra las opciones disponibles sobre 
    '''
    print("-------OPCIONES------")
    print("1-Ver archivos en Google Drive")
    print("2-Ver archivos descargados")
    print("3-Salir")
    range= 3
    opcion=validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        diccionary = {}
        print("---------Archivos que se encuentran en tu cuenta de gogle drive---------")
        diccionary = show_remote_folders_and_files()
        search_in_remote_folders(diccionary)

    elif opcion==2:
        borrar_pantalla()
        print("---------Archivos que se encuentran en tu carpeta principal---------")
        show_local_folders_and_files()
        results = search_local_folders()
        print("")

def dowload_menu()->None:
    print("-------OPCIONES------")
    print("1-Descargar archivos")
    print("2-Salir ")
    #print("3-Salir")
    #print("2-Descargar carpetas")
    print("")
    range= 2
    opcion=validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        diccionary_files = {}
        dowload_files(diccionary_files)

    #elif opcion == 2:

def create_archives_menu():
    print("-------OPCIONES------")
    print("1-Crear una carpeta")
    print("2-Crear un archivo")
    print("3-Salir")
    range= 3
    opcion = validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        create_local_and_remote_folders()

    elif opcion == 2:
        borrar_pantalla()
        create_remote_and_local_files()
    
def upload_menu():
    print("-------OPCIONES------")
    print("1-Subir un archivo")
    print("2-Salir")
    range= 2
    opcion = validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        upload_files()




