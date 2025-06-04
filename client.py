import socket
from config import HOST, PORT

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_socket(self):
        try:
            self.socket.connect((HOST, PORT))
        except Exception as error:
            print(f"Ocurrio un error al conectarse al servidor: {error}") 

    def send_msg(self, msg):
        try:
            self.socket.send(msg.encode("utf-8"))
        except Exception as error:
            print(f"Ocurrio un error al enviar el mensaje al servidor: {error}") 

    def received_msg_from_server(self):
        try: 
            data = self.socket.recv(1024)
            print(f"Respuesta del servidor: {data.decode("utf-8")}")
        except Exception as error:
            print(f"Ocurrio un error al recibir el mensaje del servidor: {error}") 

    def start(self):
        try:
            self.connect_socket()
            while True:
                self.received_msg_from_server()
                msg_to_send = input("# ")
                self.send_msg(msg_to_send)
        except Exception as error:
            print(f"Ocurrió un error durante la ejecución: {error}")
        finally:
            self.socket.close()


client = Client()
client.start()