import socket
import re
import time
import json
import codecs
from datetime import timedelta
from datetime import datetime

class Client:

    SERVER = "irc.chat.twitch.tv"
    PORT = 6667

    PING_MSG = "PING :tmi.twitch.tv"
    PONG_MSG = "PONG :tmi.twitch.tv"

    def __init__(self, nickname, token, channel, callback, sleep_s=0.1, recv_size=2048):
        self.sock = socket.socket()
        self.sock.connect((self.SERVER, self.PORT))
        self.sock.send(f"PASS {token}\n".encode("utf-8"))
        self.sock.send(f"NICK {nickname}\n".encode("utf-8"))
        self.sock.send(f"JOIN #{channel}\n".encode("utf-8"))
        self.sock.send("CAP REQ :twitch.tv/tags\n".encode("utf-8"))

        self.ping_t = datetime.now()
        self.dec = codecs.getincrementaldecoder("utf-8")()

        self.recv_size = recv_size
        self.channel = channel
        self.callback = callback
        self.sleep_s = sleep_s
        
    def listen(self):
        buffer = ""
        while True:
            buffer += self.dec.decode(self.sock.recv(self.recv_size))
            msg_list = buffer.split("\n")
            buffer = msg_list.pop()
            
            for msg in msg_list:
                msg = msg.replace("\r", "")
                if msg == self.PING_MSG:
                    self.ping_t = datetime.now()
                    self.sock.sendall(f"{self.PONG_MSG}\n".encode("utf-8"))
                else:
                    self.callback(msg)
            
            if datetime.now() - self.ping_t > timedelta(minutes=5):
                self.sock.sendall("{}\n".format(self.PING_MSG).encode("utf-8"))
            
            time.sleep(self.sleep_s)  


RE_TAG_MSG = r"@(?P<tags>.+?) :(?P<user>.+?)!.+? PRIVMSG #(?P<channel>.+?) :(?P<message>.+)"

def proc_msg(msg):
    if (m := re.match(RE_TAG_MSG, msg)):
        return \
        {
            "channel": m.group("channel"),
            "user": m.group("user"),
            "message": m.group("message"),
            "tags": {t[0]:t[1] for t in [tag.split("=") for tag in m.group("tags").split(";")]}
        }

def print_msg(msg):
    if (m := proc_msg(msg)):
        print(json.dumps(m, indent=4))
