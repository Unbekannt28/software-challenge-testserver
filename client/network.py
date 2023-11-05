# client/network.py

import json
import socket
from time import sleep

class Client():
    header_length = 16
    login_message = '{"message":"login"}'

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.establish_connection()

    def establish_connection(self):
        not_connected = True
        while not_connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
            except ConnectionRefusedError:
                print("Server refused connection\nreconnecting in 10 seconds...")
                sleep(10)
                continue

            msg = self.recv_msg()
            if msg["message"] != "connection_established":
                print("Server sent unexpected data\nreconnecting in 10 seconds...")
                sleep(10)
                continue
            
            self.send_msg(self.login_message)
            not_connected = False
    
    def send_msg(self, msg):
        try:
            msg_length = len(msg)
            msg = str(msg_length) + (self.header_length-msg_length) * " " + msg
            self.socket.send(msg.encode("utf-8"))
        except:
            print("Connection was reset\nreconnecting in 10 seconds...")
            sleep(10)
            self.establish_connection()

    def recv_msg(self):
        try:
            receiving_message = True
            full_message = ""
            
            msg = self.socket.recv(16)
            message_length = len(msg[:self.header_length])

            while receiving_message:
                full_message += self.socket.recv(16).decode("utf-8")
                if len(full_message) == message_length:
                    receiving_message = False

            print(full_message, len(full_message))
            try:
                return json.loads(full_message)
            except json.JSONDecodeError:
                return {"message": "error"}
        except ConnectionResetError:
            print("Connection was reset\nreconnecting in 10 seconds...")
            sleep(10)
            self.establish_connection()