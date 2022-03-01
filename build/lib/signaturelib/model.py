from click import echo
from flask import session
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_production = "mysql+pymysql://sql3475611:Ld1FUlXC1e@sql3.freemysqlhosting.net/sql3475611?charset=utf8"
connection_dev = "mysql+pymysql://root:@localhost/signature_bd?charset=utf8"
engine = create_engine(connection_production)
Base = declarative_base(engine)

class File(Base):
    
    __tablename__ = 'file'
    __table_args__ = {'autoload':True}

class User(Base):
    
    __tablename__ = 'user'
    __table_args__ = {'autoload':True}

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

        self.signature = None

    @orm.reconstructor
    def init_on_load(self):
        sessionbd = SessionBD()
        
        self.signature = sessionbd.get_session().query(File).filter_by(id=self.signature_id).first()


class Signature_request(Base):
    
    __tablename__ = 'signature_request'
    __table_args__ = {'autoload':True}
    
    def __init__(self, user_id, document_id, subject):
        self.user_id = user_id
        self.document_id = document_id
        self.subject = subject

        self.document = None
        self.user = None
    
    @orm.reconstructor
    def init_on_load(self):
        sessionbd = SessionBD()

        self.document = sessionbd.get_session().query(File).filter_by(id=self.document_id).first()
        self.user = sessionbd.get_session().query(User).filter_by(id=self.user_id).first()

class Signature_request_user(Base):
    
    __tablename__ = 'signature_request_user'
    __table_args__ = {'autoload':True}

    def __init__(self, request_id, user_id, pos_x, pos_y, num_page):
        self.request_id = request_id
        self.user_id = user_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.num_page = num_page

        self.signature_request = None
        self.user = None
    
    @orm.reconstructor
    def init_on_load(self):
        sessionbd = SessionBD()

        self.signature_request = sessionbd.get_session().query(Signature_request).filter_by(id=self.request_id).first()
        self.user = sessionbd.get_session().query(User).filter_by(id=self.user_id).first()

class SessionBD():
    session = None

    def get_session(self):
        if SessionBD.session == None:
            metadata = Base.metadata
            Session = sessionmaker(bind=engine)
            SessionBD.session = Session()
            return SessionBD.session
        return SessionBD.session
