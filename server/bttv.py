import requests

import socket
import requests.packages.urllib3.util.connection as urllib3_cn

def allowed_gai_family():
    """
     https://github.com/shazow/urllib3/blob/master/urllib3/util/connection.py
    """
    family = socket.AF_INET
    return family

urllib3_cn.allowed_gai_family = allowed_gai_family


def get_channel_emotes(broadcaster_id):
    ae = requests.get("http://api.betterttv.net/3/cached/users/twitch/{}".format(broadcaster_id), timeout=1).json()
    return ae["channelEmotes"] + ae["sharedEmotes"]

def get_global_emotes():
    return requests.get("http://api.betterttv.net/3/cached/emotes/global", timeout=1).json()

def get_emote_names(emotes):
    return [e["code"] for e in emotes]
