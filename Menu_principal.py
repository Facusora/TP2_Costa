import os 
import Funciones_de_Gogle_drive
import pandas as pd
import Funciones_de_Gmail
import Sistema_de_Archivos

def borrar_pantalla():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def validar_menu() -> int:
    '''
    Pre: Pide un numero en un rango
    Post: Te responde si el numero esta en el rango
    '''
    number = input("Ingrese una opcion: ")                        
    while not number.isnumeric() or (int(number)) >8 or (int(number)) <1 :
        print("")
        print("Esa opcion no es valida!")
        print("")
        number = input("Ingrese una opcion valida:")

    return int(number)

def main()->None:
    opcion=0
    while opcion !=8:
        borrar_pantalla()
        print("-----MENU PRINCIPAL-----")
        print("1. Listar archivos de la carpeta actual")
        print("2. Crear un archivo")
        print("3. Subir un archivo.")
        print("4. Descargar un archivo.")
        print("5. Sincronizar.")
        print("6. Generar carpetas de una evaluacion.")
        print("7. Actualizar entregas de alumnos vıa mail.")
        print("8. Salir.")
        opcion=validar_menu()   

        if opcion==1:
            borrar_pantalla()
            Funciones_de_Gogle_drive.file_list_menu()
        
        elif opcion==2:
            borrar_pantalla()
            Funciones_de_Gogle_drive.create_archives_menu()
        
        elif opcion==3:
            borrar_pantalla()
            Funciones_de_Gogle_drive.upload_menu()
        
        elif opcion==4:
            borrar_pantalla()
            Funciones_de_Gogle_drive.dowload_menu()
        
        elif opcion==5:
            print("5")
        
        elif opcion==6:
            borrar_pantalla()
            Funciones_de_Gmail.traer_informacion()
            Sistema_de_Archivos.Descomprimir_Zips()
        
        elif opcion==7:
            print("7")

main()