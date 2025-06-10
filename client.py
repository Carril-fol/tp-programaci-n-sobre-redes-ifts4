import socket
import threading
from config import HOST, PORT

class Client:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        """
        Esta función tiene como fin mandarle un mensaje al servidor
        """
        try:
            while True:
                message = input("# ")
                self.socket.send(message.encode('utf-8'))
                if message == "6":
                    self.socket.close()
                    break
        except Exception as error:
            print(f"Ocurrio un error al mandar un mensaje: {error}")
            
    def recieve_msg(self):
        """
        Esta función tiene como fin recibir mensajes enviados desde el servidor
        """
        try:
            while True:
                response = self.socket.recv(1024).decode('utf-8')
                if not response:
                    break
                print(response)
        except (OSError, Exception) as error:
            pass

    def start(self):
        """
        Esta función permite poner en funcionamiento el socket del cliente para conectarse al servidor predeterminado.
        Utiliza dos hilos, uno para recibir la información y otro para enviarla.
        """
        try:
            # Conexión al servidor
            self.socket.connect((HOST, PORT))
            print("Conectado al servidor")

            # Hilo de recibir informacion del servidor
            threading.Thread(target=self.recieve_msg, daemon=True).start()

            threading.Thread(target=self.send_msg, daemon=True).start()
            
            # Funcion que permite enviar datos al servidor
            self.send_msg()
        except KeyboardInterrupt:
            print("\n[Desconectado por usuario]")
        except Exception as e:
            print(f"[Error] Conexión fallida: {e}")
        finally:
            self.socket.close()
            print("[Conexión cerrada]")

cliente = Client()
cliente.start()