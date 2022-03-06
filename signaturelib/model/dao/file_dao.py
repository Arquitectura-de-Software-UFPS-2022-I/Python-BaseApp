
from typing import List

import requests
from ..dto.model_dto import File

import os 

class FileDAO :
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
    
    def create(self,path_file, name_file) -> File:
        url = '/api/v1/files/'
        

        data = {

            'name': name_file
        }
        file = {'file': open(path_file, 'rb')}
        response = requests.post(self.baseUrl+url, data=data, files=file)

        if response.status_code == 200 or response.status_code == 201 :
            file = File()
            file.from_json(response.json())
            return file
        else :
            print(response)
            return None
        
    def get_all(self):
        url = '/api/v1/files/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            files = []
            for file in response.json() :
                file_dto = File()
                file_dto.from_json(file)
                files.append(file_dto)
            return files
        else :
            print(response)
            return None
    
    def get_by_id(self, id):
        url = '/api/v1/files/'+str(id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            file = File()
            file.from_json(response.json())
            return file
        else :
            print(response)
            return None


    def delete(self, id):
        url = '/api/v1/files/'+str(id)+'/'
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(self.baseUrl+url, headers=headers)

        if response.status_code == 200 :
            file = File()
            file.from_json(response.json())
            return file
        else :
            print(response)
            return None
    
    
