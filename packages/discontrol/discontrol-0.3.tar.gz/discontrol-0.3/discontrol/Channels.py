import requests
from discontrol.Client import Client
from discontrol.Http import DiscordRequest
class Category:
  def __init__(self, CategoryId : int,client : Client):
    pass
class Channel:
  def __init__(self, ChannelId : int, client : Client):
    http = DiscordRequest({},f"Channels/{ChannelId}",client.token)
    request = http.patch()
    rq = request.json()
    self.ChannelId = rq['id']
    self.GuildId = rq['guild_id']
    self.ChannelName = rq['name']
    self.Type = rq['type']
    self.Client = client
    global token
    token = client.token
  def SendMessage(self,Message):
    return self.Client.send_message(self.ChannelId,Message)
    