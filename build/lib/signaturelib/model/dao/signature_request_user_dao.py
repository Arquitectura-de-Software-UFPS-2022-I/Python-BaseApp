
from typing import List

import requests
from ..dto.model_dto import SignatureRequestUser

class SignatureRequestUserDAO :

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
    
    def create(self, signature_request: SignatureRequestUser) -> SignatureRequestUser:
        url = '/api/v1/signature_request_users/'

        data = signature_request.to_json()
        print(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.baseUrl+url, json=data, headers=headers)

        if response.status_code == 200 or response.status_code == 201 :
            signature_request = SignatureRequestUser()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
    
    def get_all(self) -> List[SignatureRequestUser]:
        url = '/api/v1/signature_request_users/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_requests = []
            for signature_request in response.json() :
                signature_request_dto = SignatureRequestUser()
                signature_request_dto.from_json(signature_request)
                signature_requests.append(signature_request_dto)
            return signature_requests
        else :
            print(response)
            return None
    
    def get_by_id(self, id) -> SignatureRequestUser:
        url = '/api/v1/signature_request_users/'+str(id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_request = SignatureRequestUser()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
        
    def update(self, signature_request: SignatureRequestUser) -> SignatureRequestUser:
        url = '/api/v1/signature_request_users/'+str(signature_request.id)+'/'

        data = signature_request.to_json()
        print(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.put(self.baseUrl+url, json=data, headers=headers)

        if response.status_code == 200 :
            signature_request = SignatureRequestUser()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
    
    def delete(self, id) -> bool:
        url = '/api/v1/signature_request_users/'+str(id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            return True
        else :
            print(response)
            return False
    

    
    def get_by_signature_request(self, signature_request_id) -> List[SignatureRequestUser]:
        url = '/api/v1/signature_request_users_by_request/'+str(signature_request_id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_requests = []
            for signature_request in response.json() :
                signature_request_dto = SignatureRequestUser()
                signature_request_dto.from_json(signature_request)
                signature_requests.append(signature_request_dto)
            return signature_requests
        else :
            print(response)
            return None
    
    def get_by_user_id(self, user_id):
        url = '/api/v1/signature_request_users_by_user/'+str(user_id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_requests = []
            for signature_request in response.json() :
                signature_request_dto = SignatureRequestUser()
                signature_request_dto.from_json(signature_request)
                signature_requests.append(signature_request_dto)
            return signature_requests
        else :
            print(response)
            return None
    
 
      