from typing import List

import requests
from ..dto.model_dto import SignatureRequest

class SignatureRequestDAO :

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def create(self, signature_request: SignatureRequest) -> SignatureRequest:
        url = '/api/v1/signature_requests/'

        data = signature_request.to_json()
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.baseUrl+url, json=data, headers=headers)

        if response.status_code == 200 or response.status_code == 201 :
            signature_request = SignatureRequest()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
    
    def get_all(self) -> List[SignatureRequest]:
        url = '/api/v1/signature_requests/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_requests = []
            for signature_request in response.json() :
                signature_request_dto = SignatureRequest()
                signature_request_dto.from_json(signature_request)
                signature_requests.append(signature_request_dto)
            return signature_requests
        else :
            print(response)
            return None
    
    def get_by_id(self, id) -> SignatureRequest:
        url = '/api/v1/signature_requests/'+str(id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_request = SignatureRequest()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
    
    def update(self, signature_request: SignatureRequest) -> SignatureRequest:
        url = '/api/v1/signature_requests/'+str(signature_request.id)+'/'

        data = signature_request.to_json()
        headers = {'Content-Type': 'application/json'}
        response = requests.put(self.baseUrl+url, data=data, headers=headers)

        if response.status_code == 200 :
            signature_request = SignatureRequest()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None

    def delete(self, signature_request: SignatureRequest) -> SignatureRequest:
        url = '/api/v1/signature_requests/'+str(signature_request.id)+'/'

        headers = {'Content-Type': 'application/json'}
        response = requests.delete(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_request = SignatureRequest()
            signature_request.from_json(response.json())
            return signature_request
        else :
            print(response)
            return None
        
    
    def get_by_user(self, user_id) -> List[SignatureRequest]:
        url = '/api/v1/signature_requests_by_user/'+str(user_id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            signature_requests = []
            for signature_request in response.json() :
                signature_request_dto = SignatureRequest()
                signature_request_dto.from_json(signature_request)
                signature_requests.append(signature_request_dto)
            return signature_requests
        else :
            print(response)
            return None