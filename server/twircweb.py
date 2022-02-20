import threading
import json
import yaml
from yaml import Loader
import time

import srv, twirc
import twitch, bttv, ffz

class TwitchIRC():
    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f.read(), Loader=Loader)
        
        self.c = twirc.Client(config["irc"]["username"], config["irc"]["token"], config["irc"]["channel"], lambda m: self.p(m))
        self.t = threading.Thread(target = self.c.listen)
        self.t.daemon = True
        self.t.start()

        self._lock = threading.Lock()
        self.ms = []

    def p(self, m):
        self._lock.acquire()
        if (pm := twirc.proc_msg(m)):
            self.ms.append(pm)
            print(json.dumps(pm, indent=4))
        self._lock.release()

    @srv.route('/lm')
    def handle_lm(self, p):
        self._lock.acquire()
        r = self.ms
        self.ms = []
        self._lock.release()
        return r

class TwitchEmotes():
    def __init__(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f.read(), Loader=Loader)

        tc = twitch.init_client(config['api']['id'], config['api']['secret'])
        id = tc.get_account_id("xqcow")

        self.twitch_emotes = tc.get_channel_emotes(id)["data"] + tc.get_global_emotes()["data"]
        self.bttv_emotes = bttv.get_channel_emotes(id) + bttv.get_global_emotes()
        self.ffz_emotes = ffz.get_channel_emotes(id) + ffz.get_global_emotes()
    
    @srv.route('/twitch')
    def handle_twitch_emotes(self, p):
        r = {}
        for e in self.twitch_emotes:
            eurl = e["images"]["url_1x"].split("/")
            eurl[-2] = "dark"
            eurl[-3] = "default"
            r[e["name"]] = "/".join(eurl)
        
        return r
    
    @srv.route('/bttv')
    def handle_bttv_emotes(self, p):
        return {e["code"]: "https://cdn.betterttv.net/emote/{}/1x".format(e["id"]) for e in self.bttv_emotes}
    
    @srv.route('/ffz')
    def handle_ffz_emotes(self, p):
        return {e["name"]: "https:" + e["urls"]["1"] for e in self.ffz_emotes}


if __name__ == "__main__":
    srv.run(TwitchEmotes(), port = 8080)
    srv.run(TwitchIRC(), port = 8081)
    while True:
        time.sleep(1)
