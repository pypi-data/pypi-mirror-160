from http import client
import requests
import asyncio

BaseUrl = "http://api.rankgun.works"



class Bot: 

    def __init__(self, username, password, Type):
        self.name = username
        self.password = password
        self.Type = Type

    async def Promote(self, subject):
     U = self.name
     P = self.password
     T = self.Type
     url = f"{BaseUrl}/developer/{T}/promote"
     print(url)
     payload = {
         "subject": subject,
         "username": U,
         "password": P
     }
     response = requests.request("GET", url, params=payload)
     print(response.json())
     return(response.json())

    async def Demote(self, subject):
     U = self.name
     P = self.password
     T = self.Type
     url = f"{BaseUrl}/developer/{T}/demote"
     print(url)
     payload = {
         "subject": subject,
         "username": U,
         "password": P
     }
     response = requests.request("GET", url, params=payload)
     print(response.json())
     return(response.json())

    async def SetRank(self, subject, Rank):
     U = self.name
     P = self.password
     T = self.Type
     url = f"{BaseUrl}/developer/{T}/setrank"
     print(url)
     payload = {
         "subject": subject,
         "rank": Rank,
         "username": U,
         "password": P
     }
     response = requests.request("GET", url, params=payload)
     print(response.json())
     return(response.json())

    async def Shout(self, Text):
     U = self.name
     P = self.password
     T = self.Type
     url = f"{BaseUrl}/developer/elite/shout"
     print(url)
     payload = {
         "text": Text,
         "username": U,
         "password": P
     }
     response = requests.request("GET", url, params=payload)
     print(response.json())
     return(response.json())

    async def Exile(self, subject):
     U = self.name
     P = self.password
     T = self.Type
     url = f"{BaseUrl}/developer/elite/exile"
     print(url)
     payload = {
         "subject": subject,
         "username": U,
         "password": P
     }
     response = requests.request("GET", url, params=payload)
     print(response.json())
     return(response.json())
