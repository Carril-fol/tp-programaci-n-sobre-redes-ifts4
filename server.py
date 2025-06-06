import socket
import uuid
import threading
from config import MENU

HOST = '127.0.0.1'
PORT = 12345

clients = []

class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def users_online(self):
        if len(clients) == 0:
            return "No hay nadie conectado."
        return "\n".join(f"\n🧑‍💻 {user["username"]}\n" for user in clients)

    def register(self, client, username: str, password: str):
        if not username or not password:
            raise Exception("Ingrese los datos correspondientes")
        
        user_id = str(uuid.uuid4())
        data_user = {
            "id": user_id, 
            "username": username.lower(),
            "password": password,
            "client": client
        }
        clients.append(data_user)
        return True

    def authenticate(self, username: str, password: str):
        for user in clients:
            if user["username"] == username and user["password"] == password:
                return user
        return None

    def shutdown_socket(self):
        try:
            self.socket.close()
            print("Server apagado")
        except Exception as error:
            print(f"Ocurrio un error al apagar el server: {error}")

    def conversation_with_client(self, client, address):
        # Variable de control de usuario
        user = None
        try:
            # Mientras sea verdadero...
            while True:
                # Envio del menu al cliente
                client.send(MENU.encode("utf-8"))

                # Respuesta del cliente recibida por el servidor
                response = client.recv(1024).decode("utf-8").strip()
                if not response:
                    break
                
                if response == "1":
                    client.send("\nIngrese su nombre de usuario".encode("utf-8"))
                    username = client.recv(1024).decode("utf-8")

                    client.send("\nIngrese cual va a ser su contraseña".encode("utf-8"))
                    password = client.recv(1024).decode("utf-8")

                    if self.register(client, username, password):
                        client.send(f"\n¡Usuario registrado con exito!\n".encode("utf-8"))
                    else:
                        client.send(f"\nError al crear el usuario, pruebe otra vez...\n".encode("utf-8"))

                elif response == "2":
                    client.send("\nIngrese su nombre de usuario: ".encode("utf-8"))
                    username = client.recv(1024).decode("utf-8")

                    client.send("\nIngrese su contraseña: ".encode("utf-8"))
                    password = client.recv(1024).decode("utf-8")
                    
                    # Si esta autenticado, entonces...
                    if self.authenticate(username, password):
                        user = username
                        client.send(f"\nBienvenido {user}.\n".encode("utf-8"))
                    # Si no..
                    else:
                        client.send("\nUsuario o contraseña incorrectos.\n".encode("utf-8"))

                elif response == "3":
                    client.send("\n¿A quien desea enviarle un mensaje?".encode("utf-8"))
                    username_from_user_to_send = client.recv(1024).decode("utf-8")

                elif response == "4":
                    client.send("\n🟢 - Usuarios en linea:".encode("utf-8"))
                    # Se llama a la función .users_online()
                    online_users = self.users_online()
                    # Se envia la información de los usuarios conectados.
                    client.send(online_users.encode())

                elif response == "5":
                    pass

                elif response == "7":
                    client.close()

            client.close()
            print("Conexion cerrada")
        except Exception as error:
            print(f"Ocurrio un error a: {error}")
        except KeyboardInterrupt as error:
            print(f"Desconexion por parte del cliente")
            self.shutdown_socket()

    def start(self):
        try:
            # Setteo del socket a un HOST y un PORT
            self.socket.bind((HOST, PORT))
            # Configuracion de escuchar del servidor
            self.socket.listen(5)
            print("🟢 - ¡Server encendido!")

            while True:
                # Manejo del cliente y su direccion IP
                client, address = self.socket.accept()
                print(f"- Conexión desde {address}")

                # Hilo para manejar las respuestas de los clientes que se conecten al servidor
                threading_clients = threading.Thread(target=self.conversation_with_client, args=(client, address, ))
                threading_clients.start()

        except Exception as error:
            print(f"Ocurrio un error al configurar el socket: {error}")
            self.shutdown_socket()
        except KeyboardInterrupt as error:
            print(f"Servidor apagado")
            self.shutdown_socket()

a = Server()
a.start()
