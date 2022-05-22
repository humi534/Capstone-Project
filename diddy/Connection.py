
import socket
import json

class Connection:
    def __init__(self, server_order):
        self.server_order = server_order
        self.HEADER = 16
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        #self.SERVER = socket.gethostbyname(socket.gethostname())  #"192.168.0.3" #mettre l'adresse ip du serveur
        #self.SERVER = '192.168.1.17'
        self.SERVER = '192.168.5.103'
        self.ADDR = (self.SERVER, self.PORT)

        #Setup the connection to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        print("Connection established")
        
    def send(self, msg):
        print("sending: ", msg)
        try: 
            msg = json.dumps(msg)
        except: 
            raise Exception("The message must be encoded as a json object")

        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def wait_server_msg(self):
        while True:
            print("waiting for message")
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                server_msg = self.client.recv(msg_length).decode(self.FORMAT)
                server_msg = json.loads(server_msg)
                print("server message: ", server_msg)
                self.server_order.change_msg(server_msg)