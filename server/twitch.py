import requests

class Client:

    URL_GET_USERS = 'https://api.twitch.tv/helix/users'
    URL_GET_CHANNEL_EMOTES = 'https://api.twitch.tv/helix/chat/emotes'
    URL_GET_GLOBAL_EMOTES = 'https://api.twitch.tv/helix/chat/emotes/global'

    def __init__(self, id, token):
        self.id = id
        self.token = token
    
    def get_auth_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Client-Id': self.id
        }
    
    def get_users(self, id=[], login=[]):
        return requests.get(self.URL_GET_USERS, params={'id': id, 'login': login}, headers=self.get_auth_headers()).json()
    
    def get_channel_emotes(self, broadcaster_id):
        return requests.get(self.URL_GET_CHANNEL_EMOTES, params={'broadcaster_id': broadcaster_id}, headers=self.get_auth_headers()).json()
    
    def get_global_emotes(self):
        return requests.get(self.URL_GET_GLOBAL_EMOTES, headers=self.get_auth_headers()).json()

    def get_account_id(self, name):
        return self.get_users(login=[name])["data"][0]["id"]


def get_emote_names(emotes):
    return [e["name"] for e in emotes]


def init_client(id, secret, scopes=[]):
    params = {
        'client_id': id,
        'client_secret': secret,
        'grant_type': 'client_credentials',
        'scopes': ' '.join(scopes)
    }

    response = requests.post('https://id.twitch.tv/oauth2/token', data=params)

    return Client(id, response.json()['access_token'])
