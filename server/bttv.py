import requests

def get_channel_emotes(broadcaster_id):
    ae = requests.get("https://api.betterttv.net/3/cached/users/twitch/{}".format(broadcaster_id)).json()
    return ae["channelEmotes"] + ae["sharedEmotes"]

def get_global_emotes():
    return requests.get("https://api.betterttv.net/3/cached/emotes/global").json()

def get_emote_names(emotes):
    return [e["code"] for e in emotes]
