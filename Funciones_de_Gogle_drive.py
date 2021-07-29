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
    Post: Crea la carpeta principal del usuario en caso de que no la tenga creada
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
                            'Word':'.docx',
                            'Power point':'.ppt',
                            'Excel':'.xls'}

    borrar_pantalla()
    print("-------TIPOS DE EXTENSIONES DISPONIBLES-----------")
    for keys in diccionary_extensions:
        print(keys) #BIBLIOTECA PARA MEJORAR EL PRINT DEL DICCIONARIO

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
        file_name = input ("\nIngrese el nombre del archivo que quiere:")

        if file_name !="":
            
            extension, mimetype = select_extension()
            file_format = file_name + extension
            print(mimetype)
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

    file_metadata = {'name' :f'{file_name}',
                    'mimeType' :f'{mimeType}' }       

    file = drive_service.files().create(body=file_metadata, fields='id').execute()

def select_mymetype(mimeType:str)->str:
    '''
    Pre: -
    Post: Returna la extension del archivo a crear
    '''
    diccionary_mimeType = {'Texto':'.txt',
                            'Word':'application/vnd.google-apps.document',
                            'Power point':'application/vnd.google-apps.presentation',
                            'Excel':'application/vnd.google-apps.spreadsheet'}
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

def search_local_folders()->str:
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
    
    folder_id = f'{driveid}'
    query = f"parents='{folder_id}' "
    
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response=service.files(),list(q=query).execute()
        files.extend(response.get('nextPageToken'))
        nextPageToken = response.get('nextPageToken')

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
            dictionary.update({id:name}) #EN EL CASO DE QUE EL DIC NO CONTENGA LOS ARCHIVOS LE HACEMOS UN UPDATE
                                #name:id hago una prueba
    return dictionary

def search_in_remote_folders(diccionary_folders:dict)->str:
    '''
    Pre: Pide el ingreso de datos
    Post: Revisa si la carpeta ingresada existe y muestra sus datos
    '''
    service = service__drive.obtener_servicio()
    continue_search=input("\nQuiere buscar una carpeta?(si/no):")

    if continue_search=="si":start=True

    else:
        start=False 
        folder_id = ""

    while start:
        folder_id=input("\nEscriba el id de la carpeta (dicha id puede copiar y pegarse):")
        print("\n")
        if folder_id in diccionary_folders.keys():            
            query = f"parents='{folder_id}'"

            response=service.files().list(q=query).execute()
            files = response.get('files')
            nextPageToken=response.get('nextPageToken')
            diccionary_folders = folders_and_archives(response,diccionary_folders)
            
            while nextPageToken:
                response = service.files(),list(q=query).execute()
                files.extend(response.get('nextPageToken'))
                nextPageToken = response.get('nextPageToken')
            change_format(files)


        elif folder_id not in diccionary_folders.keys():
            print("Esa carpeta no existe")

        continue_search=input("\nQuiere seleccionar otra carpeta?(si/no):")

        if continue_search=="si" and folder_id in diccionary_folders.keys():
            diccionary_folders = folders_and_archives(response,diccionary_folders) #LE SUMAMOS LOS ARCHIVOS AL DIC EN CADA INTERACCION

        elif continue_search!="si":
            start=False

    return folder_id

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

def download_remote_files(service:str, fileId:str, filePath:str)->None:
    request = service.files().get_media(fileId=fileId)

    fh = io.FileIO(filePath, mode='wb')
    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024)
        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries = 2)
        if status:
            print("Descargando %d%%." % int(status.progress() * 100))
    finally:
        fh.close()

def download_folder(service, fileId, destinationFolder)->None:
    if not os.path.isdir(destinationFolder):
        os.mkdir(path=destinationFolder)

    results = service.files().list(pageSize=300,q="parents in '{0}'".format(fileId),fields="files(id, name, mimeType)").execute()

    items = results.get('files', [])

    for item in items:
        itemName = item['name']
        itemId = item['id']
        itemType = item['mimeType']
        filePath = destinationFolder + "/" + itemName

        if itemType == 'application/vnd.google-apps.folder': 
            download_folder(service, itemId, filePath) 

        elif itemType.startswith('application/vnd'):#SI ES UN ARCHIVO DE GOOGLE NO LO DESCARGAMOS DEBIDO A LOS ERRORES
            print("Este tipo de archivos no pueden descargarse {0}".format(itemName))

        elif not itemType.startswith('application/vnd.google-apps.folder'): #SI EL ARCHIVO NO ES UNA CARPETA LO DESCARGAMOS
            download_remote_files(service, itemId, filePath)

def download_file_request()->None:
    '''
    Pre: Pide el ingreso de datos
    Post: Descarga el archivo que seleccione el usuario 
    '''
    download_another_file =""
    continue_downloading = ""
    done = True
    diccionary_files={}
    service = service__drive.obtener_servicio()

    while done:
        borrar_pantalla()
        start = True

        diccionary_files = show_remote_folders_and_files()
        folder_id = search_in_remote_folders(diccionary_files)

        while start:
                file_id= input ("\nIngrese la id del archivo que quiere descargar (se puede copiar y pegar dicha id):")

                if file_id in diccionary_files.keys() :
                    file_name = diccionary_files[file_id]
                    file_name = f'{file_name}'
                    file_id = f'{file_id}'

                    route = choose_dowload_location()
                    filePath = route + f'\\{file_name}'
                    download_remote_files(service, file_id, filePath) #LLAMAMOS A LA FUNCION PARA DESCARGAR UN ARCHIVO

                else: 
                    print("\nEse archivo no existe\n")
                    download_another_file = input ("Quiere intentar descargar otro archivo de esta carpeta(si/no)?:")
                if download_another_file != "si": 
                    start = False
                    continue_downloading = input("\nQuiere volver a la carpeta principal de descargas(si/no)?:")

                if continue_downloading !="si": done = False  

def download_folder_request():
    diccionary_files ={}
    service = service__drive.obtener_servicio()
    folder_name = ""
    continue_downloading = ""
    download_another_folder = ""
    done = True

    while done :
        borrar_pantalla()
        start = True
        diccionary_files = show_remote_folders_and_files()
        search_in_remote_folders(diccionary_files)

        while start:
            folder_id = input("\nIngrese el id de la carpeta que quiere descargar:")

            if folder_id in diccionary_files:
                folde_name = diccionary_files[folder_id]
                folder_id = f'{folder_id}'
                
                destinationFolder = choose_dowload_location() + f'\\{folder_name}'
                download_folder(service, folder_id, destinationFolder)
                download_another_folder= input("\nQuiere descargar otra carpeta? (si/no):")

            else: 
                print("\nNo selecciono correctamente la carpeta ")
                download_another_folder= input("\nQuiere descargar otra carpeta? (si/no):")

            if download_another_folder !="si":
                start = False
                continue_downloading = input("\nQuiere volver a la carpeta principal de descargas(si/no)?:")

            if continue_downloading != "si": done = False
            
def choose_dowload_location()->str:
    borrar_pantalla()
    print("\n-Seleccione la carpeta donde desea descargar el archivo\n")
    show_local_folders_and_files()
    results = search_local_folders()

    return results

def search_folder_upload()->str:
    '''
    Pre: Pide una serie de datos para la busqueda de carpetas
    Post: Sube un archivo a la carepta elegida por el usuario
    '''
    diccionary_files = {}
    folder_id = ""
    service = service__drive.obtener_servicio()

    search_in_folders = input ("Quieres elegir una carpeta donde se suba el archivo (si/no)?:")

    if search_in_folders =="si":
        diccionary_files = show_remote_folders_and_files()
        folder_id2 = search_in_remote_folders(diccionary_files)
        folder_id = input ("Ingrese el id de la carpeta donde quiere subir el archivo:")
    
    elif folder_id in diccionary_files:
        folder_name = diccionary_files[folder_id]
        print(f"Archivo subido a la carpeta {folder_name}")

    if folder_id == "" or folder_id not in diccionary_files or search_in_folders !="si":
        folder_id =  service.files().get(fileId='root').execute()['id']
        #SI LA ID LLEEGA VACIA O NO ESTA EN EL DICCIONARIO SUBE EL ARCHIVO DIRECTAMENTE A LA CARPETA PRINCIPAL DE DRIVE
    
    return folder_id


def prepare_to_upload(direction:str,file_name:str)->None:
    '''
    Pre: -
    Post: Sube un archivo a la carpeta principal de google drive
    '''
    service = service__drive.obtener_servicio()
    folder_id = search_folder_upload()

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
            continue_upload = input ("\nQuiere intentarlo de nuevo (si/no)?:")
        
        if continue_upload == "no":
            start = False
            file_name = ""
            direction = ""

        else : print ("")

    return direction, file_name

def upload_files()->None:
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
        diccionary_files = {}
        print("---------Archivos que se encuentran en tu cuenta de gogle drive---------")
        diccionary_files = show_remote_folders_and_files()
        search_in_remote_folders(diccionary_files)

    elif opcion==2:
        borrar_pantalla()
        print("---------Archivos que se encuentran en tu carpeta principal---------")
        show_local_folders_and_files()
        results = search_local_folders()
        print("")

def dowload_menu()->None:
    print("-------OPCIONES------")
    print("1-Descargar archivos")
    print("2-Descargar carpeta ")
    print("3-Salir")
    range= 3
    opcion=validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        diccionary_files = {}
        download_file_request()

    elif opcion == 2:
        borrar_pantalla()
        print("-----------Descarga de carpetas-----------")
        download_folder_request()

def create_archives_menu()->None:
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
        print("--------Crear archivos--------\n")
        create_remote_and_local_files()
    
def upload_menu()->None:
    print("-------OPCIONES------")
    print("1-Subir un archivo")
    print("2-Salir")
    range= 2
    opcion = validar_rango(range)

    if opcion == 1:
        borrar_pantalla()
        upload_files()






