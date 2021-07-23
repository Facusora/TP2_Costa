import base64
import service__gmail
import os
import csv
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart



def leer_csv(nombre_archivo) -> dict:

  
    datos1 = []
    
    with open(nombre_archivo) as file_csv:
        csv_reader = csv.DictReader(file_csv)
        for linea in csv_reader:
            datos1.append(linea)
    return datos1


def obtenerDocentes(archivo2) -> dict:
    datos2 = []
    with open(archivo2) as file_csv:
        csv_reader = csv.DictReader(file_csv)
        for linea in csv_reader:
            datos2.append(linea)
    print()

    return datos2

def obtenerAlumnos(archivo3,informacion_total,gmail_service) -> dict:
    datos3 = []

    with open(archivo3) as file_csv:
        csv_reader = csv.DictReader(file_csv)
        for linea in csv_reader:
            datos3.append(linea)
    print()
    print(datos3)
    mandar_mensaje(informacion_total,datos3,gmail_service)

    return datos3




def mandar_mensaje(informacion_total,datos3,gmail_service) -> None:
    
    padrones_dic = {}


    for i in datos3:
        
        padrones_dic[i["padron"]] = i["Nombre_alumno"]
       
    
    for j in informacion_total:
        print(j)
        
        
        mimeMessage = informacion_total[j][1]
        
        

        if j not in padrones_dic.keys():
            print("ERROR")
            emailMsg = "ERROR"
            mimeMessage = MIMEMultipart()
            mimeMessage["to"] = informacion_total[j][1]
            mimeMessage["subject"] = "vuelva a intentar"
            mimeMessage.attach(MIMEText(emailMsg,"plain"))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

            message = gmail_service.users().messages().send(userId="me", body = {"raw": raw_string}).execute()
            
            print(message)
            
            print("your message has been sent") 
            
                

            
        else :
            mensajeGmail_OK(gmail_service,informacion_total,j)


     
def mensajeGmail_OK(gmail_service,informacion_total,j) -> None:
    
    

            print("OK")
           
            emailMsg = "ok"
            mimeMessage = MIMEMultipart()
            mimeMessage["to"] = informacion_total[j][1]
            mimeMessage["subject"] = "bien"
            mimeMessage.attach(MIMEText(emailMsg,"plain"))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

            message = gmail_service.users().messages().send(userId="me", body = {"raw": raw_string}).execute()
            print(message)
            print("your message has been sent")


def traer_informacion() -> None:
    gmail_service = service__gmail.obtener_servicio()


    
    #https://gmail.googleapis.com/gmail/v1/users/{userId}/messages/{id}
    codigos_id = []
    informacion_total  = {}
    
    result = gmail_service.users().messages().list(userId='me', q="after:2021/07/22").execute()   
    j = 0
    
        
    for j in range(len(result["messages"])): 
        j+=1
    
        id_mensaje = result["messages"][(j-1)]["id"]  
        codigos_id.append(id_mensaje)

        result2 = gmail_service.users().messages().get(userId='me', id = id_mensaje).execute()
        
        body = result2["payload"]["headers"][6]["value"]
        body = body[1:-1]

    
        asunto = result2["payload"]["headers"][19]["value"]  
        bien_asunto = asunto.split(",")
        

        punto_zip = result2["snippet"]
        bien_zip = punto_zip.split(".")
        

        informacion_total[bien_asunto[1]] = [bien_asunto[0],body,bien_zip[1]]


    print(informacion_total)
   
    print()

    print(codigos_id)
    print()
    

    archivo = "docente-alumnos.csv"
    archivo2 = "docentes.csv"
    archivo3 = "alumnos.csv"

    
    print(leer_csv(archivo))
    print(obtenerDocentes(archivo2))
    obtenerAlumnos(archivo3,informacion_total,gmail_service)


traer_informacion()






