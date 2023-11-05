# server/network.py

import json
import socket

class Server():
    header_length = 16
    welcome_message = '{"message":"connection_established"}'

    def __init__(self, port):
        self.client1 = None
        self.client1_address = ""
        self.client2 = None
        self.client2_address = ""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", port))
        self.socket.listen(2)
    
    def send_msg(self, client, msg):
        msg_length = len(msg)
        msg = str(msg_length) + (self.header_length-msg_length) * " " + msg
        client.send(msg.encode("utf-8"))

    def recv_msg(self, client):
        receiving_message = True
        full_message = ""
        
        msg = client.recv(16)
        message_length = len(msg[:self.header_length])

        while receiving_message:
            full_message += client.recv(16).decode("utf-8")
            if len(full_message) == message_length:
                receiving_message = False
        return json.loads(full_message)



    def establish_connections(self):
        if self.client1 != None:
            self.send_msg(self.client1, "alive_check")
        if self.client2 != None:
            self.send_msg(self.client2, "alive_check")
        
        if self.client1 != None and self.client2 != None:
            return

        while True:
            clientsocket, address = self.socket.accept()
            self.send_msg(clientsocket, self.welcome_message)
            msg = self.recv_msg(clientsocket)
            
            if msg["message"] != "login":
                clientsocket.close()
                continue
            
            if self.client1 == None:
                self.client1 = clientsocket
            else:
                self.client2 = clientsocket
            
            if self.client1 != None and self.client2 != None:
                break