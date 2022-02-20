import requests

def get_twitch_room(broadcaster_id):
    return requests.get("https://api.frankerfacez.com/v1/room/id/{}".format(broadcaster_id)).json()

def get_channel_emotes(broadcaster_id):
    room = get_twitch_room(broadcaster_id)
    return room["sets"][str(room["room"]["set"])]["emoticons"]

def get_global_emotes():
    r = requests.get("https://api.frankerfacez.com/v1/set/global").json()
    emotes = [eset["emoticons"] for eset in [r["sets"][str(setid)] for setid in r["default_sets"]]]
    return [emote for sl in emotes for emote in sl]

def get_emote_names(emotes):
    return [e["name"] for e in emotes]
