
class File():
    def __init__(self,id = None , name = None, uuid_image = None, file = None ,create_date  = None):
        self.id = id
        self.name = name
        self.uuid_image = uuid_image
        self.file = file
        self.create_date = create_date
    
    def from_json(self,json):
        self.id = json['id']
        self.name = json['name']
        self.uuid_image = json['uuid_image']
        self.file = json['file']
        self.create_date = json['create_date']
        return self

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid_image': self.uuid_image,
            'file': self.file,
            'create_date': self.create_date
        }

    def __str__(self):
        return f'{self.id} - {self.name} - {self.uuid_image} - {self.file} - {self.create_date}'

class User():
    def __init__(self, id = 0, username = None, email = None, password = None, full_name = None, signature = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name
        self.signature = signature

    def from_json(self,json):
        self.id = json['id']
        self.username = json['username']
        self.email = json['email']
        self.password = json['password']
        self.full_name = json['full_name']
        self.signature = json['signature']
        return self
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'full_name': self.full_name,
            'signature': self.signature
        }

    def __str__(self):
        return f'{self.id} - {self.username} - {self.email} - {self.password} - {self.full_name} - {self.signature}'

    

class SignatureRequest():
    def __init__(self, id = None, subject = None, document = None,user = None,create_date = None):
        self.id = id
        self.subject = subject
        self.document = document
        self.user = user
        self.create_date = create_date
    
    def from_json(self,json):
        self.id = json['id']
        self.subject = json['subject']
        self.document = json['document']
        self.user = json['user']
        self.create_date = json['create_date']
        return self
    
    def to_json(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'document': self.document,
            'user': self.user,
            'create_date': self.create_date
        }
        
    def __str__(self):
        return f'{self.id} - {self.subject} - {self.document} - {self.user} - {self.create_date}'
    


class SignatureRequestUser():
    def __init__(self, id = None, request = None, user = None, pos_x = None, pos_y = None, num_page = None, signed = False , signature_date = None, created_date = None):
        self.id = id
        self.request = request
        self.user = user
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.num_page = num_page
        self.signed = signed
        self.signature_date = signature_date
        self.created_date = created_date
    
    def from_json(self,json):
        self.id = json['id']
        self.request = json['request']
        self.user = json['user']
        self.pos_x = json['pos_x']
        self.pos_y = json['pos_y']
        self.num_page = json['num_page']
        self.signed = json['signed']
        self.signature_date = json['signature_date']
        self.created_date = json['created_date']
        return self

    def to_json(self):
        return {
            'id': self.id,
            'request': self.request,
            'user': self.user,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'num_page': self.num_page,
            'signed': self.signed,
            'signature_date': self.signature_date,
            'created_date': self.created_date
        }

    def __str__(self):
        return f'{self.id} - {self.request} - {self.user} - {self.pos_x} - {self.pos_y} - {self.num_page} - {self.signed} - {self.signature_date} - {self.created_date}'
    