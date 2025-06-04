import socket
import threading
from config import MENU

HOST = '127.0.0.1'
PORT = 12345

class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def _user_already_exists(self, address):
        return address in self.clients

    def _save_user_data(self, address):
        try:
            if self._user_already_exists(address):
                return False
            self.clients.append(address)
            return True
        except Exception as error:
            print(f"Ocurrio un error al momento de guardar los datos: {error}")

    def shutdown_socket(self):
        try:
            self.socket.close()
            print("Server apagado")
        except Exception as error:
            print(f"Ocurrio un error al apagar el server: {error}")

    def handle_client(self):
        try:
            client_socket, address = self.socket.accept()
            while True:
                # Envio de menu al usuario
                client_socket.send(MENU.encode("utf-8"))
                
                # Mensaje enviada por el cliente
                data = client_socket.recv(1024)
                # Hilo del cliente
                threading.Thread(target=client_socket)
                print(f"Respuesta del cliente: {data.decode("utf-8")}")
        except KeyboardInterrupt:
            print("\nServidor detenido manualmente.")
        except Exception as error:
            print(f"Ocurrió un error durante la ejecución: {error}")

    def start(self):
        try:
            self.socket.bind((HOST, PORT))
            self.socket.listen(5)
            print("Server encendido")
        except Exception as error:
            print(f"Ocurrio un error al configurar el socket: {error}")
            self.socket.close()
        self.handle_client()

server = Server()
server.start()