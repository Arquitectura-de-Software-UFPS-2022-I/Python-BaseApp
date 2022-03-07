from typing import List
from ..dto.model_dto import User, File, SignatureRequest, SignatureRequestUser
import requests

class UserDAO() :
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def create(self,user: User) -> User:
        url = '/api/v1/users/'
        headers = {'Content-Type': 'application/json'}
        data = user.to_json()
        response = requests.post(self.baseUrl+url, headers=headers, json=data)

        if response.status_code == 200 or response.status_code == 201 :
            user = User()
            user.from_json(response.json())
            return user
        else :
            print(response)
            return None
        
    def update(self,user: User) -> User:
        url = '/api/v1/users/'+str(user.id)+'/'
        headers = {'Content-Type': 'application/json'}
        data = user.to_json()
        response = requests.put(self.baseUrl+url, headers=headers, json=data)

        if response.status_code == 200 :
            user = User()
            user.from_json(response.json())
            return user
        else :
            print(response)
            return None
    
    def get_by_id(self,id: int) -> User:
        url = '/api/v1/users/' + str(id)+'/'
        response = requests.get(self.baseUrl+url)

        if response.status_code == 200 :
            user = User()
            user.from_json(response.json())
            return user
        else :
            print(response)
            return None
    
    def get_all(self) -> List[User]:
        url = '/api/v1/users/'
        response = requests.get(self.baseUrl+url)

        if response.status_code == 200 :
            users =  [User().from_json(user) for user in response.json()]
            return users
        else :
            print(response)
            return None
    
    def get_by_username_and_password(self,username: str, password: str) -> User:
        url = '/api/v1/auth/user/'
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}
        response = requests.post(self.baseUrl+url, headers=headers, json=data)

        if response.status_code == 200 :
            user = User()
            user.from_json(response.json())
            return user
        else :
            print(response)
            return None