
from signaturelib.services import get_list_signature_request_user_by_request_id_and_signed, get_list_signature_request_user_by_user_id_and_signed, get_signature_request, get_user_login, validate_signature, approve_signature, get_file_pdf, get_request_signature_by_user, list_users, register_request_signature_user,register_user,get_user,insert_signature,register_request_signature
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
    9. Mis solicitudes pendientes
    10. Listado de firmas pendientes en una solicitud
    11. Listado de firmas aprobadas en una solicitud
    12. Mi historico de firmas
    13. Test api
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
        user = get_user_login(username, password)
        print(user)
    
    if option == '4':
        doc = input('Document path: ')
        image = open(doc,'rb')

        #if validate_signature(input("BASE 64:")):
        user_id = int(input('User ID: '))
        insert_signature(user_id, image.name, image.read())
        #else:
        #    print("El archivo no corresponde a una firma")
    
    if option == '5':
        doc = input('Document path: ')
        pdf = open(doc,'rb')        
        user_id = int(input('User ID: '))
        subject = input("Subject: ")

        register_request_signature(user_id, pdf.name, pdf.read(), subject)

    if option == '6':
        request_id = int(input('Request ID: '))
        user_id = int(input('User ID: '))
        pos_x = int(input('Pos X: '))
        pos_y = int(input('Pos Y: '))
        num_page = int(input('Num Page: '))
        register_request_signature_user(request_id, user_id, pos_x, pos_y, num_page)

    if option == '7' :
        
        user_id = int(input('User ID: '))
        request_signature = get_request_signature_by_user(user_id)
        print("ID || SUBJECT")
        for request in request_signature:
            print(request.id,request.subject)
        
        print(" Seleccione una solicitud")
        request_id = int(input())
        pdf = get_file_pdf(request_id)

        with open('doc_firmado.pdf', 'wb') as f:
            f.write(pdf)
        
    if option == '8':
        request_id = int(input('Request ID: '))
        approve_signature(request_id)
        print("Firma aprobada")
    
    if option == '9':
        user_id = int(input('User ID: '))

        request_signature_users = get_list_signature_request_user_by_user_id_and_signed(user_id, False)
        print('Request ID || Request Signature ID || Subject')
        for request_signature_user in request_signature_users:
            print(
                request_signature_user.signature_request.id, 
                request_signature_user.id, 
                request_signature_user.signature_request.subject
            )

    if option == '10':
        request_id = int(input('Request ID: '))

        request_signature_users = get_list_signature_request_user_by_request_id_and_signed(request_id=request_id, signed=False)
        print('Request ID || Request Signature ID || Subject || User for signed')
        for request_signature_user in request_signature_users:
            print(
                request_signature_user.signature_request.id, 
                request_signature_user.id, 
                request_signature_user.signature_request.subject,
                request_signature_user.user.name
            )
    
    if option == '11':
        request_id = int(input('Request ID: '))

        request_signature_users = get_list_signature_request_user_by_request_id_and_signed(request_id=request_id, signed=True)
        print('Request ID || Request Signature ID || Subject || User for signed')
        for request_signature_user in request_signature_users:
            print(
                request_signature_user.signature_request.id, 
                request_signature_user.id, 
                request_signature_user.signature_request.subject,
                request_signature_user.user.name
            )
    
    if option == '12':
        user_id = int(input('User ID: '))

        request_signature_users = get_list_signature_request_user_by_user_id_and_signed(user_id, True)
        print('Request ID || Request Signature ID || Date Signed')
        for request_signature_user in request_signature_users:
            print(
                request_signature_user.signature_request.id, 
                request_signature_user.id, 
                request_signature_user.signature_request.subject, 
                request_signature_user.signature_date
            )
    
    if option == '13':
        image = input('Image path: ')
        print(validate_signature(image))