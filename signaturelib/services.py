import os, base64
from typing import List
from signaturelib.model import SessionBD,User,File,Signature_request,Signature_request_user
import fitz , smtplib, datetime, requests

sessionbd = SessionBD()
session = sessionbd.get_session()

def register_user(name: str, email: str, username: str, password: str) -> User:
    """
    Registra un nuevo usuario {table_name=User}

    :name: str, nombre del usuario
    :email: str, email del usuario
    :username: str, username del usuario, restriccion len(username) <= 10
    :passwrod: str, password del usuario

    :return: User object
    """
    user = User(name=name, email=email, username=username, password=password)
    session.add(user)
    session.commit()
    
    return user


def validate_signature(image: str) -> bool:
    """
    Valida si la imagen efectivamente corresponde a una firma

    :image: str, ruta de la imagen a verificar

    :return: True si la imagen corresponde a una firma, False de lo contrario
    """

    url = "http://52.240.59.172:8000/signature-recognition/"

    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    payload = {"image": encoded_string}
    
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()['class_label'] == 1

    return False

def list_users() -> list[User]:
    """
    Lista los usuario {table_name=User} registrados en la base de datos

    :return: [] lista de usuarios
    """

    users = session.query(User).all()
    return users


def get_user_login(username: str, password: str) -> User:
    """
    Obtiene un usuario {table_name=User} dado el username y password

    :username: str, username del usuario
    :password: str, password del usuario

    :return: User object
    """

    user = session.query(User).filter_by(username=username,password=password).first()
    return user

def register_request_signature(user_id: int, name_file: str, file: bytes, subject: str) -> Signature_request:
    """
    Registra una solicitud de firma asociando su respectivo documento {table_name=Signature_request}

    :user_id: int, id del usuario que registra la solicitud
    :file: bytes, archivo en formato de bytes al cual se asociara con la solicitud
    :subject: str, descripcion de la solicitud, este mismo sera enviado como Asunto en el email
    cuando el usuario propietario le solicite a otro usuario su firma

    :return: Signature_request object
    """
    saved_file = insert_file(name_file, file)
    request_signature = Signature_request(user_id=user_id, document_id=saved_file.id, subject=subject)
    session.add(request_signature)
    session.commit()

    return request_signature

def get_request_signature_by_user(user_id: int) -> list[Signature_request]:
    """
    Obtiene la lista de solicitudes por documento {table_name=Signature_request} 
    que un usuario ha realizado

    :user_id: int, id del usuario
    
    :return: [] lista de solicitudes por documento
    """

    request_signatures = session.query(Signature_request).filter_by(user_id=user_id).all()
    return request_signatures

def register_request_signature_user(request_id: int, user_id: int, pos_x: int, pos_y: int, num_page: int) -> Signature_request_user:
    """
    Registra una solicitud de firma {table_name=Signature_request_user}
    y enviara un email para notificar al usuario que se le solicito firmar

    :request_id: int, id del Signature_request al cual se va a asociar esta solicitud de firma
    :user_id: int, id del usuario al cual se le solicitara la firma
    :pos_x: int, posicion X donde firmara el usuario
    :pos_y: int, posicion Y donde firmara el usuario
    :num_page: int, numero de pagina donde firmara el usuario

    :return: Signature_request_user object
    """
    signature_request_user = Signature_request_user(request_id=request_id, user_id=user_id, pos_x=pos_x, pos_y=pos_y, num_page=num_page)
    session.add(signature_request_user)
    session.commit()

    request_signature = get_signature_request(request_id)
    send_email(user_origin_id=request_signature.user_id, user_destination_id=user_id, request_id=request_id)

    return signature_request_user


def list_files() -> list[File]:
    """
    Lista los archivos {table_name=File} registrados en la base de datos

    :return: File object
    """
    files = session.query(File).all()
    return files


def insert_file(name_file: str, file: bytes) -> File:
    """
    Metodo generico para el registro de archivos {table_name=File}.
    Su proposito es modularizar el registro de firmas y pdf's

    :file: BufferedReader, archivo que sera guardado

    :return: File object
    """
    file = File(file=file, name=name_file) 
    session.add(file)
    session.commit()
    return file

def insert_signature(user_id: int, name_file: str, image: bytes) -> User:
    """
    Registra la firma y la asocia con su respectivo usuario

    :user_id: int, usuario que registra la firma
    :image: BufferedReader, archivo de la firma

    :return: User_object
    """
    user = session.query(User).filter_by(id=user_id).first()
    user.signature_id =  insert_file(name_file, image).id
    session.commit()

    return user

def get_user(user_id: int) -> User:
    """
    Busca un usuario dado su id {table_name=User}

    :user_id: int, id del usuario a buscar

    :return: User object
    """
    user = session.query(User).filter_by(id=user_id).first()
    return user

def get_file(file_id: int) -> File:
    """
    Busca un archivo dado su id {table_name=File}

    :file_id: int, id del archivo a buscar

    :return: File object
    """
    file = session.query(File).filter_by(id=file_id).first()
    return file

def get_signature_request(request_id: int) -> Signature_request:
    """
    Busca una solicitud dado su id {table_name=Signature_request}

    :request_id: int, id de la solicitud a buscar

    :return: Signature_request object
    """
    request = session.query(Signature_request).filter_by(id=request_id).first()
    return request

def send_email(user_origin_id: int, user_destination_id: int, request_id: int) -> None:
    """
    Envia un email notificando al usuario que se le ha solicitado su firma

    :user_origin_id: int, id del usuario propietario de la solicitud
    :user_destination_id: int, id del usuario al que se le solicita la firma
    :request_id: int, id de la solicitud del propietario
    """
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
    

def approve_signature(request_user_signature_id: int) -> bool:
    """
    Aprueba la solicitud de firma dada a un usuario

    :request_user_signature_id: int, id de la solicitud de firma asociada al usuario que se
    le solicito la firma

    :return: True si se actualizo el registro, False de lo contrario
    El retorno se debe a que quizas el usuario este intentando firmar nuevamente
    el documento, entonces retornara False si ya se encontraba firmado
    """
    request_users_signature = session.query(Signature_request_user).filter_by(id=request_user_signature_id).first()
    if request_users_signature.signed != 1:
        request_users_signature.signed = 1
        request_users_signature.signature_date = datetime.datetime.now()
        session.commit()
        return True
    return False
    

def get_file_pdf(request_id: int) -> bytes:
    """
    Retorna el documento firmado por los usuarios que han aprobado su solicitud de firma
    asociada al solicitud registrada por el propietario

    :request_id: int, id de la solicitud del propietario

    :return: bytes, documento ya firmado en formato de bytes
    """

    request_users_signature = session.query(Signature_request_user).filter_by(request_id=request_id, signed=1).all()
    signature_request = get_signature_request(request_id)
    pdf = get_file(signature_request.document_id).file
    
    with open('temp.pdf', 'wb') as outfile:
        outfile.write(pdf)

    file_handle = fitz.open('temp.pdf')
    for request in request_users_signature:
        signature = request.user.signature.file

        with open('signature.png', 'wb') as outfile:
            outfile.write(signature)
        signature = open("signature.png", "rb").read()

        image_rectangle = fitz.Rect(20, 20, 200, 200)
        os.remove('signature.png')
        num_page = file_handle[request.num_page-1]
        num_page.insert_image(image_rectangle, stream=signature)

    file_handle.save('doc_firmado.pdf')
    file_handle.close()

    os.remove('temp.pdf')
    
    doc_file = open("doc_firmado.pdf", "rb")
    doc_bytes = doc_file.read()
    doc_file.close()

    os.remove("doc_firmado.pdf")

    return doc_bytes
    
def get_list_signature_request_user_by_user_id_and_signed(user_id: int, signed: bool) -> List[Signature_request_user]:
    """
    Lista las solicitudes de firmas que le han solicitado al usuario

    :user_id: int, id del usuario al cual le han solicitado firmas
    :signed: bool, indica si desea buscar aprobadas (True) o pendientes (False)

    :return: [Signature_request_user]

    Nota:
        Las pendientes son el requerimiento 9
        Las aprobadas son el requerimiento 12, es decir el historico
    """
    signature_request_users = session.query(Signature_request_user).filter_by(user_id=user_id, signed=1 if signed else 0).all()
    return signature_request_users

def get_list_signature_request_user_by_request_id_and_signed(request_id: int, signed: bool) -> List[Signature_request_user]:
    """
    Lista las solicitudes de firmas asociadas a una solicitud

    :request_id: int, id de la solicitud por la cual se desea buscar firmas aprobadas o pendientes
    :signed: bool, indica si desea buscar aprobadas (True) o pendientes (False)

    :return: [Signature_request_user]

    Nota:
        Las pendientes son el requerimiento 10
        Las aprobadas son el requerimiento 11
    """
    signature_request_users = session.query(Signature_request_user).filter_by(request_id=request_id, signed=1 if signed else 0).all()
    return signature_request_users