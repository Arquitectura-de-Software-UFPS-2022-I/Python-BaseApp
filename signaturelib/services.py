from signaturelib.model import loadSession,User,File,Signature_request,Signature_request_user
import io, fitz

session = loadSession()

def register_user(name,email,username,password):
    
    user = User(name=name,email=email,username=username,password=password)
    session.add(user)
    session.commit()
    
    return user


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
    return True

def register_request_signature(user_id, file_id, subject):
    request = Signature_request(user_id=user_id, document_id=file_id, subject=subject)
    session.add(request)
    session.commit()

def list_files():
    files = session.query(File).all()
    return files


def insert_file(file):
   
    file = File(file=file.read(),name=file.name) 
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


def get_file_pdf(request_id):
    request_users_signature = session.query(Signature_request_user).filter_by(request_id=request_id).all()
    signature_request = get_signature_request(request_id)
    pdf = get_file(signature_request.document_id).file
    
    file_handle = fitz.open(stream=pdf, filetype='pdf')
    
    for request in request_users_signature:
        user = get_user(request.user_id)
        signature = get_file(user.signature_id).file

        image_rectangle = fitz.Rect(request.pos_x, request.pos_y,100,100)

        num_page = file_handle[0]
        num_page.insert_image(image_rectangle, stream=signature)
    
    return file_handle

def insert_pdf(pdf):
    return insert_file(pdf)
    
