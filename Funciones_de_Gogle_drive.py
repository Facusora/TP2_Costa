import service__drive
import pickle
import os
import io
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd 


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



def show_remote_files():
    diccionary={}

    service=service__drive.obtener_servicio()
    driveid = service.files().get(fileId='root').execute()['id'] #para obtener el drive id y poder listar solo "my-drive"
    
    folder_id=f'{driveid}'
    query=f"parents='{folder_id}' "#and mimeType='application/vnd.google-apps.folder'"
    
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

    for file in response.get('files'): 
        name=file.get('name')
        id=file.get('id')  

        if id not in dictionary:
            dictionary.update({name:id}) #EN EL CASO DE QUE EL DIC NO CONTENGA LOS ARCHIVOS LE HACEMOS UN UPDATE

    return dictionary

def search_folders(diccionary_folders:dict):
    service=service__drive.obtener_servicio()
    continue_search=input("Quiere buscar en una carpeta?(si/no):")

    if continue_search=="si":
        start=True

    else: 
        start=False

    while start:
        name_folder=input("Escriba el nombre de la carpeta que desea ver:")

        if name_folder in diccionary_folders.keys():            
            name_folder=diccionary_folders[name_folder]
            folder_id=f'{name_folder}'
            query=f"parents='{name_folder}'"

            response=service.files().list(q=query).execute()
            files = response.get('files')
            nextPageToken=response.get('nextPageToken')

            while nextPageToken:
                response=service.files(),list(q=query).execute()
                files.extend(response.get('nextPageToken'))
                nextPageToken=response.get('nextPageToken')

            change_format(files)

        elif name_folder not in diccionary_folders.values():
            print("Esa carpeta no existe")

        continue_search=input("Quiere buscar otra carpeta?(si/no):")
        
        if continue_search=="si":
            start=True
            diccionary_folders = folders_and_archives(response,diccionary_folders) #LE SUMAMOS LOS ARCHIVOS AL DIC EN CADA INTERACCION

        elif continue_search!="si":
            start=False
            borrar_pantalla()

def change_format(files):
    pd.set_option('display.max_columns',100)
    pd.set_option('display.max_rows',500)
    pd.set_option('display.min_rows',500)
    pd.set_option('display.max_colwidth',150)
    pd.set_option('display.width',200)
    pd.set_option('expand_frame_repr',True)
    df = pd.DataFrame(files)
    print(df)

def file_list_menu():
    print("-------OPCIONES------")
    print("1-Ver archivos en Google Drive")
    print("2-Ver archivos descargados")
    print("")
    opcion=validar_rango()

    if opcion==1:
        borrar_pantalla()
        diccionary={}
        print("---------Archivos que se encuentran en tu cuenta de gogle drive---------")
        diccionary = show_remote_files()
        search_folders(diccionary)

    elif opcion==2:
        print("")


