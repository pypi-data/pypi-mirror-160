import requests


class DiscordRequest:
  def __init__(self,json : str,path : str,token : str):
    self.json = json
    self.token = token
    self.path = path
  def get(self):
    headers = {"Authorization": f"Bot {self.token}"}
    url = f"https://discord.com/api/v9/{self.path}"
    json = self.json
    response = requests.get(url, headers=headers, json=json)
    return response
  def patch(self):
    headers = {"Authorization": f"Bot {self.token}"}
    url = f"https://discord.com/api/v9/{self.path}"
    json = self.json
    response = requests.patch(url, headers=headers, json=json)
    return response
  def post(self):
    headers = {"Authorization": f"Bot {self.token}"}
    url = f"https://discord.com/api/v9/{self.path}"
    json = self.json
    response = requests.post(url, headers=headers, json=json)
    return response
  def put(self):
    headers = {"Authorization": f"Bot {self.token}"}
    url = f"https://discord.com/api/v9/{self.path}"
    json = self.json
    response = requests.put(url, headers=headers, json=json)
    return response
  def remove(self):
    headers = {"Authorization": f"Bot {self.token}"}
    url = f"https://discord.com/api/v9/{self.path}"
    json = self.json
    response = requests.remove(url, headers=headers, json=json)
    return response