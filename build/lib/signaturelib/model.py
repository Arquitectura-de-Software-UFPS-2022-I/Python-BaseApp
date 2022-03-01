from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:@localhost/signature_bd?charset=utf8', echo=True)
Base = declarative_base(engine)

class User(Base):
    
    __tablename__ = 'user'
    __table_args__ = {'autoload':True}


class File(Base):
    
    __tablename__ = 'file'
    __table_args__ = {'autoload':True}


class Signature_request(Base):
    
    __tablename__ = 'signature_request'
    __table_args__ = {'autoload':True}

class Signature_request_user(Base):
    
    __tablename__ = 'signature_request_user'
    __table_args__ = {'autoload':True}

def loadSession():
    
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


    
    
    
