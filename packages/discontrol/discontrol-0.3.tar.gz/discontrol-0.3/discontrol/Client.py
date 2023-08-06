import requests
from discontrol.Message import Message
from discontrol.Errors import errors
from discontrol.Status import Status
from discontrol.RequestBad import request_bad
from discontrol.Http import DiscordRequest
from discontrol.GuildUser import GuildUser


class Client:

    def __init__(self, token, show_logs: bool = True):
        self.token = token
        self.show_logs = show_logs

        TestRequest = DiscordRequest({}, 'users/@me/library', self)
        TestRequest = TestRequest.get()

        try:
            error = TestRequest.json()['message']

            if TestRequest.status_code in request_bad:
                raise errors.FailedToRunClient(
                    f'Failed to run client ({error})')
        except:
            pass

    def send_message(self, channel_id: int, content):
        Json = {'content': content}
        Headers = {'Authorization': self.token}
        Url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

        Request = requests.post(Url, json=Json, headers=Headers)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToSendMessage(
                    f'Send message error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Send message:', Request.status_code)

        id = Request.json()['id']

        return Message(id, channel_id, self)

    def set_status_icon(self, status):
        if status not in [
                Status.online, Status.idle, Status.dnd, Status.invisible
        ]:
            raise errors.InvalidStatusIcon('Invalid status icon')

        Url = 'https://discord.com/api/v9/users/@me/settings'
        Headers = {'Authorization': self.token}
        Json = {'status': status}

        Request = requests.patch(Url, headers=Headers, json=Json)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToChangeStatusIcon(
                    f'Change status icon error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Change status icon:', Request.status_code)

    def set_status_text(self, text):
        Url = 'https://discord.com/api/v9/users/@me/settings'
        Headers = {'Authorization': self.token}
        Json = {'custom_status': {'text': text}}

        Request = requests.patch(Url, headers=Headers, json=Json)

        if self.show_logs:
            if Request.status_code in request_bad:
                raise errors.FailedToChangeStatusText(
                    f'Change status text error: {Request.status_code} - ' +
                    Request.json()['message'], Request.status_code)
            else:
                print('[i] Change status text:', Request.status_code)

    def get_user(self, guild_id, user_id):
        return GuildUser(self.token, guild_id, user_id)

    def me(self):
        Request = DiscordRequest({}, f'users/@me', self.token)
        Request = Request.patch()

        class User:
            id = Request['id']
    
    def custom_request(self, type: str, json: dict, path: str):
        if type not in ['get', 'patch', 'post', 'put', 'remove']:
            raise errors.InvalidCustomRequestType('Supports only get/patch/post/put/remove')

        Request = DiscordRequest(json, path, self.token)
        if type == 'get':
            Response = Request.get()
        if type == 'patch':
            Response = Request.patch()
        if type == 'post':
            Response = Request.post()
        if type == 'put':
            Response = Request.put()
        if type == 'remove':
            Response = Request.remove()

        return Response