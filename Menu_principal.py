import os 
import Funciones_de_Gogle_drive

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
    numero = input("Ingrese una opcion: ")                        
    while not numero.isnumeric() or (int(numero)) >8 or (int(numero)) <1 :
        print("")
        print("Esa opcion no es valida!")
        print("")
        numero = input("Ingrese una opcion valida:")

    return int(numero)

opcion=0
while opcion !=8:
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
        Funciones_de_Gogle_drive.listar_archivos()
    
    elif opcion==2:
        print("2")
    
    elif opcion==3:
        print("3")
    
    elif opcion==4:
        print("4")
    
    elif opcion==5:
        print("5")
    
    elif opcion==6:
        print("6")
    
    elif opcion==7:
        print("7")