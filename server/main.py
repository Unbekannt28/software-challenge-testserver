# server/main.py

from network import Server

SERVER_PATH = "software-challenge-server/start.sh"
PORT = 13000

server = Server(PORT)

server.establish_connections()