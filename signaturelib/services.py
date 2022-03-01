import os
from signaturelib.model import loadSession,User,File,Signature_request,Signature_request_user
import io, fitz , json, smtplib, datetime

session = loadSession()

def register_user(name,email,username,password):
    
    user = User(name=name,email=email,username=username,password=password)
    session.add(user)
    session.commit()
    
    return user


def validate_signature(image):
    url = ""

def list_users():
    users = session.query(User).all()
    return users


def get_user(username,password):
    user = session.query(User).filter_by(username=username,password=password).first()
    return user



def get_request_signature_by_user(user_id):
    request_signature = session.query(Signature_request).filter_by(user_id=user_id).all()
    return request_signature

def register_request_signature_user(request_id, user_id, pos_x, pos_y, num_page):
    
    signature_request_user = Signature_request_user(request_id=request_id, user_id=user_id, pos_x=pos_x, pos_y=pos_y, num_page=num_page)
    session.add(signature_request_user)
    session.commit()
    request_signature = get_signature_request(request_id)
    send_email(user_origin_id=request_signature.user_id, user_destination_id=user_id, request_id=request_id)
    return True

def register_request_signature(user_id, file_id, subject):
    request = Signature_request(user_id=user_id, document_id=file_id, subject=subject)
    session.add(request)
    session.commit()

def list_files():
    files = session.query(File).all()
    return files


def insert_file(file):
   
    file = File(file=file.read(),name=file.name.split("/")[-1]) 
    session.add(file)
    session.commit()
    return file


def insert_signature(user_id,image):
    
    user = session.query(User).filter_by(id=user_id).first()
    user.signature_id =  insert_file(image).id
    session.commit()
    return True

def get_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

def get_file(file_id):
    file = session.query(File).filter_by(id=file_id).first()
    return file

def get_signature_request(request_id):
    request = session.query(Signature_request).filter_by(id=request_id).first()
    return request

def send_email(user_origin_id, user_destination_id, request_id):

    user_origin = get_user(user_origin_id)
    user_destination = get_user(user_destination_id)
    request = get_signature_request(request_id)
    file_pdf = get_file(request.document_id)
    

    msg = "Se le notifica que el usuario "+user_origin.name+" ha solicitado su firma para el documento "+file_pdf.name+"."
    subject = request.subject

    msg ='subject: {}\n\n{}'.format(subject, msg)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("softwarearchitecture9@gmail.com", "architecture$9")
    server.sendmail("softwarearchitecture9@gmail.com", user_destination.email, msg)
    server.quit()
    print("Correo enviado")

def approve_signature(request_users_signature_id):
    request_users_signature = session.query(Signature_request_user).filter_by(id=request_users_signature_id).first()
    request_users_signature.signed = 1
    request_users_signature.signature_date = datetime.datetime.now()
    session.commit()
    return True

def get_file_pdf(request_id):
    request_users_signature = session.query(Signature_request_user).filter_by(request_id=request_id, signed=1).all()
    signature_request = get_signature_request(request_id)
    pdf = get_file(signature_request.document_id).file
    print(len(request_users_signature))
    with open('temp.pdf', 'wb') as outfile:
        outfile.write(pdf)

    file_handle = fitz.open('temp.pdf')
    for request in request_users_signature:

        user = get_user(request.user_id)
        signature = get_file(user.signature_id).file

        with open('signature.png', 'wb') as outfile:
            outfile.write(signature)
        signature = open("signature.png", "rb").read()

        image_rectangle = fitz.Rect(20, 20,100,100)
        print(file_handle)
        os.remove('signature.png')
        num_page = file_handle[request.num_page-1]
        num_page.insert_image(image_rectangle, stream=signature)
    file_handle.save('doc_firmado.pdf')
    file_handle.close()
   #  return file_handle
    os.remove('temp.pdf')
    

def insert_pdf(pdf):
    return insert_file(pdf)
    
