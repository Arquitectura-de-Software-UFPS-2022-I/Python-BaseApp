
from signaturelib.services import approve_signature, get_file, get_file_pdf, get_request_signature_by_user, list_users, register_request_signature_user,register_user,get_user,insert_signature,insert_pdf,register_request_signature
import os,time

option = '5'

while option != '0' : 
     
    print('''
    1. Lists all users 
    2. Register a new user 
    3. Log in 
    4. Insert signature 
    5. Ingresar PDF 
    6. Solicitar Firma 
    7. Generar PDF 
    8. Aprobar Firma

    ''')

    option = input()
    os.system('cls')   
    
    if option == '1':
        users = list_users()
        os.system('cls')
        for user in users:
            print(user.name)
        

    if option == '2':
        name = input('Name: ')
        email = input('Email: ')
        username = input('Username: ')
        password = input('Password: ')
        register_user(name,email,username,password)

    if option == '3':
        username = input('Username: ')
        password = input('Password: ')
        user = get_user(username,password)
        print(user)
    
    if option == '4':
        doc = input('Document path: ')
        image = open(doc,'rb')
        print(type(image))        
        user_id = int(input('User ID: '))
        insert_signature(user_id,image)
    
    if option == '5':
        doc = input('Document path: ')
        pdf = open(doc,'rb')        
        user_id = int(input('User ID: '))
        file = insert_pdf(pdf)
        register_request_signature(user_id,file.id,'Tema generico')

    if option == '6':
        request_id = int(input('Request ID: '))
        user_id = int(input('User ID: '))
        pos_x = int(input('Pos X: '))
        pos_y = int(input('Pos Y: '))
        num_page = int(input('Num Page: '))
        register_request_signature_user(request_id,user_id,pos_x,pos_y,num_page)

    if option == '7' :
        
        user_id = int(input('User ID: '))
        request_signature = get_request_signature_by_user(user_id)
        print("ID || SUBJECT")
        for request in request_signature:
            print(request.id,request.subject)
        
        print(" Seleccione una solicitud")
        request_id = int(input())
        pdf = get_file_pdf(request_id)
        
    if option == '8':
        request_id = int(input('Request ID: '))
        approve_signature(request_id)
        print("Firma aprobada")
    