import socket
import os, sys
from threading import Thread
from datetime import datetime


class utils:
    def returnDate(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string

    def save_log(self, output):
        with open("logs.txt", "a") as file:
            file.write(output)
    def switch(self, key):
        key = key.lower().rstrip()
        respostas = {
            "user": "admin",
            "pass": "admin",
            "service": "FTP",
            "test": "asda"
        }
        try:
            return respostas[key] + "\n"
        except:
            return None
    def fake_return(self, key):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("google.com.br", 80))
        s.send(key.encode())
        resposta = s.recv(2048)
        if not resposta: return None
        return resposta
class Th(Thread, utils):
    def __init__(self, con, client, close):
        Thread.__init__(self)
        self.con = con
        self.client = client
        self.close = close
    def run(self):
        while(True):
            msg = self.con.recv(2048)
            if not msg: break
            try:
                self.save_log(f"{self.returnDate()} - {self.client[0]} - {msg.decode()}\n")
                print(f"{self.returnDate()} - {self.client[0]} - {msg.decode()}\n")
                retorno = self.fake_return(msg.decode())
                if retorno != None:
                    print(f"RETORNO - {self.returnDate()} - {self.client[0]} - {retorno}")
                    self.con.send(retorno)
            except:
                self.save_log(f"{self.returnDate()} - {self.client[0]} - {msg}\n")
                print(f"{self.returnDate()} - {self.client[0]} - {msg}\n")
class Honey(utils):
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.retorn_padrao = "FTP"
        self.tcp = None
    def listen(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind((self.host, self.port))
        tcp.listen(1)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp = tcp
        while True:
            con, client = tcp.accept()
            self.save_log(f"{self.returnDate()} - Conexão aberta com {client[0]} - \n")
            print(f"{self.returnDate()} - Conexão aberta com {client[0]} - \n")
            a = Th(con, client, self.close)
            a.start()
    def close(self):
        self.tcp.close()