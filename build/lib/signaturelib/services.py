import os, base64
from typing import List
from .model.dao.user_dao import UserDAO
from .model.dao.signature_request_dao import SignatureRequestDAO
from .model.dao.signature_request_user_dao import SignatureRequestUserDAO
from .model.dao.file_dao import FileDAO
import requests

from .model.dto.model_dto import SignatureRequest, SignatureRequestUser, User, File

urlBase = 'http://52.240.59.172:8000'

user_dao = UserDAO(urlBase)
signature_request_dao = SignatureRequestDAO(urlBase)
signature_request_user_dao = SignatureRequestUserDAO(urlBase)
file_dao = FileDAO(urlBase)

def register_user(name: str, email: str, username: str, password: str) -> User:
    """
    Requerimiento 1
    Registra un nuevo usuario {table_name=User}

    :name: str, nombre del usuario
    :email: str, email del usuario
    :username: str, username del usuario, restriccion len(username) <= 10
    :passwrod: str, password del usuario

    :return: User object
    """
    user = User(full_name=name, email=email, username=username, password=password)
    
    
    return user_dao.create(user)


def validate_signature(image: str) -> bool:
    """
    Requerimiento 4
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

    return user_dao.get_all()


def get_user_login(username: str, password: str) -> User:
    """
    Requerimiento 2
    Obtiene un usuario {table_name=User} dado el username y password

    :username: str, username del usuario
    :password: str, password del usuario

    :return: User object
    """

    return user_dao.get_by_username_and_password(username, password)

def register_request_signature(user_id: int, name_file: str, file: str, subject: str) -> SignatureRequest:
    """
    Requerimiento 5
    Registra una solicitud de firma asociando su respectivo documento {table_name=Signature_request}

    :user_id: int, id del usuario que registra la solicitud
    :name_file: str, ruta del archivo PDF
    :subject: str, descripcion de la solicitud, este mismo sera enviado como Asunto en el email
    cuando el usuario propietario le solicite a otro usuario su firma

    :return: Signature_request object
    """
    saved_file = insert_file(name_file, file)
    
    request_signature = SignatureRequest(user = user_id, document =saved_file.id, subject= subject)
 
    return signature_request_dao.create(request_signature)

def get_request_signature_by_user(user_id: int) -> list[SignatureRequest]:
    """
    Obtiene la lista de solicitudes por documento {table_name=Signature_request} 
    que un usuario ha realizado

    :user_id: int, id del usuario
    
    :return: [] lista de solicitudes por documento
    """

    
    return signature_request_dao.get_by_user(user_id)

def register_request_signature_user(request_id: int, user_id: int, pos_x: int, pos_y: int, num_page: int) -> SignatureRequestUser:
    """
    Requerimiento 7
    Registra una solicitud de firma {table_name=Signature_request_user}
    y enviara un email para notificar al usuario que se le solicito firmar

    :request_id: int, id del Signature_request al cual se va a asociar esta solicitud de firma
    :user_id: int, id del usuario al cual se le solicitara la firma
    :pos_x: int, posicion X donde firmara el usuario
    :pos_y: int, posicion Y donde firmara el usuario
    :num_page: int, numero de pagina donde firmara el usuario

    :return: Signature_request_user object
    """
    signature_request_user = SignatureRequestUser(request=request_id, user=user_id, pos_x=pos_x, pos_y=pos_y, num_page=num_page)


    return signature_request_user_dao.create(signature_request_user)


def list_files() -> list[File]:
    """
    Lista los archivos {table_name=File} registrados en la base de datos

    :return: File object
    """
    return file_dao.get_all()


def insert_file(name_file: str, file: str) -> File:
    """
    Metodo generico para el registro de archivos {table_name=File}.
    Su proposito es modularizar el registro de firmas y pdf's

    :file: BufferedReader, archivo que sera guardado

    :return: File object
    """

    return file_dao.create(file,name_file)


def insert_signature(user_id: int, name_file: str, image: str) -> User:
    """
    Requerimiento 3
    Registra la firma y la asocia con su respectivo usuario

    :user_id: int, usuario que registra la firma
    :image: BufferedReader, archivo de la firma

    :return: User_object
    """
    user = user_dao.get_by_id(user_id)
    
    user.signature =  insert_file(name_file, image).id

    return user_dao.update(user)


def get_user(user_id: int) -> User:
    """
    Busca un usuario dado su id {table_name=User}

    :user_id: int, id del usuario a buscar

    :return: User object
    """
    return user_dao.get_by_id(user_id)


def get_file(file_id: int) -> File:
    """
    Busca un archivo dado su id {table_name=File}

    :file_id: int, id del archivo a buscar

    :return: File object
    """
    return file_dao.get_by_id(file_id)


def get_signature_request(request_id: int) -> SignatureRequest:
    """
    Busca una solicitud dado su id {table_name=Signature_request}

    :request_id: int, id de la solicitud a buscar

    :return: Signature_request object
    """
    return signature_request_dao.get_by_id(request_id)

    

def approve_signature(request_user_signature_id: int) -> bool:
    """
    Requerimiento 8
    Aprueba la solicitud de firma dada a un usuario

    :request_user_signature_id: int, id de la solicitud de firma asociada al usuario que se
    le solicito la firma

    :return: True si se actualizo el registro, False de lo contrario
    El retorno se debe a que quizas el usuario este intentando firmar nuevamente
    el documento, entonces retornara False si ya se encontraba firmado
    """
    request_users_signature = signature_request_user_dao.get_by_id(request_user_signature_id)
    if not request_users_signature.signed :
        request_users_signature.signed = True
        signature_request_user_dao.update(request_users_signature)
        return True
    return False
    

def get_file_pdf(request_id: int) -> bytes:
    """
    Requerimiento 9
    Retorna el documento firmado por los usuarios que han aprobado su solicitud de firma
    asociada al solicitud registrada por el propietario

    :request_id: int, id de la solicitud del propietario

    :return: bytes, documento ya firmado en formato de bytes

    Nota: Cualquier excepcion que produzca este metodo sera si o si debido a dos factores:
    1. Las posiciones X y/o Y son mayores al ancho o alto respectivamente
    2. El numero de pagina no existe
    """

    url = urlBase+'/api/v1/generate_pdf/' + str(request_id)+ '/'
    response = requests.get(url)

    return response.content

    
def get_list_signature_request_user_by_user_id_and_signed(user_id: int, signed: bool) -> List[SignatureRequestUser]:
    """
    Requerimiento 9 y 12
    Lista las solicitudes de firmas que le han solicitado al usuario

    :user_id: int, id del usuario al cual le han solicitado firmas
    :signed: bool, indica si desea buscar aprobadas (True) o pendientes (False)

    :return: [Signature_request_user]

    Nota:
        Las pendientes son el requerimiento 9
        Las aprobadas son el requerimiento 12, es decir el historico
    """
    
    signature_request_users = signature_request_user_dao.get_by_user_id(user_id)

    for rq in signature_request_users:
        if rq.signed != signed:
            signature_request_users.remove(rq)

    
    return signature_request_users

def get_list_signature_request_user_by_request_id_and_signed(request_id: int, signed: bool) -> List[SignatureRequestUser]:
    """
    Requerimiento 10 y 11
    Lista las solicitudes de firmas asociadas a una solicitud

    :request_id: int, id de la solicitud por la cual se desea buscar firmas aprobadas o pendientes
    :signed: bool, indica si desea buscar aprobadas (True) o pendientes (False)

    :return: [Signature_request_user]

    Nota:
        Las pendientes son el requerimiento 10
        Las aprobadas son el requerimiento 11
    """
    signature_request_users = signature_request_user_dao.get_by_signature_request(request_id)

    for rq in signature_request_users:
        if rq.signed != signed:
            signature_request_users.remove(rq)
    
    return signature_request_users
            