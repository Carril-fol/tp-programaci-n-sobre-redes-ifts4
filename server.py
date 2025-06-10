import socket
import threading

from config import MENU, HOST, PORT

clients = []

class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def users_online(self):
        """
        Esta función permite ver los usuarios conectados.

        Returns:
        -------
        str: Retorna el nombre de todos los usuarios conectados.
        """
        if len(clients) == 0:
            return "No hay nadie conectado."
        return "\n".join(f"\n{user["username"]}\n" for user in clients)

    def register(self, client, username: str, password: str):
        """
        Esta función permite a los usuarios registrarse en el servidor.

        Args:
        ----
        client: Instancia de cliente del usuario.
        username (str): Nombre del usuario.
        password (str): Contraseña del usuario.

        Returns:
        -------
        bool: Retorna una booleano que representa que se creo efectivamente la cuenta del usuario.
        """
        if not username or not password:
            raise Exception("Ingrese los datos correspondientes")
        
        data_user = {
            "username": username.lower(),
            "password": password,
            "client": client
        }
        clients.append(data_user)
        return True
    
    def disconnect(self, user_instance):
        """
        Esta función permite desconectarse a los usuarios.

        Args:
        ----
        user_instance: Instancia del usuario.
        """
        for user in clients:
            if user["username"] == user_instance:
                clients.remove(user)
                print(f"{user_instance} se desconecto del servidor.")
                break

    def authenticate(self, username: str, password: str):
        """
        Esta función permite autenticar al usuario

        Args:
        ----
        username (str): Nombre del usuario
        password (str): Contraseña del usuario

        Returns:
        -------
        user: Retorna la instacia de usuario si es que existe.
        None: Retorna None si no existe el usuario.
        """
        for user in clients:
            if user["username"] == username and user["password"] == password:
                return user
        return None
    
    def send_msg_to_all_users_online(self, message, user_instance):
        """
        Esta función permite enviar mensaje a todos los usuarios conectados.

        Args:
        ----
        message: Mensaje del usuario.
        user_instance: Instancia de usuario emisor.
        """
        try:
            for user in clients:
                user["client"].send(f"\n[+] Mensaje de {user_instance}: {message}\n".encode())
        except Exception as error:
            print(f"Error enviando a {user['username']}: {error}")
            clients.remove(user)

    def send_msg_to_user(self, message, user_issuer, user_receiver):
        """
        Esta función sirve para mandar mensajes entre usuarios

        Args:
        ----
        message (str): Mensaje del usuario.
        user_issuer: Instancia de usuario del emisor
        user_receiver: Instancia del cliente del usuario que va a recibir el mensaje.
        """
        try:
            for user in clients:
                if not user["username"]:
                    raise Exception("No se encontro al usuario ingresado")
                user["client"].send(f"\n[+] Mensaje de {user_issuer}: {message}\n".encode())
        except Exception as error:
            print(f"Error enviando a {user['username']}: {error}")
            clients.remove(user)

    def shutdown_socket(self):
        """
        Esta función permite apagar el servidor.
        """
        try:
            self.socket.close()
            print("Server apagado")
        except Exception as error:
            print(f"Ocurrio un error al apagar el server: {error}")

    def conversation_with_client(self, client):
        """
        Esta función permite la conversación con el cliente y el servidor, 
        permitiendo interactuar con diferentes funciones de este.

        Args:
        ----
        client: Instancia de cliente del usuario.
        """
        # Variable de control de usuario
        user = None
        try:
            # Mientras sea verdadero...
            while True:
                # Envio del menu al cliente
                client.send(MENU.encode("utf-8"))

                # Respuesta del cliente recibida por el servidor
                response = client.recv(1024).decode().strip()
                if not response:
                    break
                parts = response.split(" ")
                
                # Si la respuesta es 1, entonces...
                if response == "1":
                    client.send("\nIngrese su nombre de usuario".encode("utf-8"))
                    username = client.recv(1024).decode("utf-8")

                    client.send("\nIngrese cual va a ser su contraseña".encode("utf-8"))
                    password = client.recv(1024).decode("utf-8")

                    if self.register(client, username, password):
                        client.send(f"\n¡Usuario registrado con exito!\n".encode("utf-8"))
                        user = username
                        client.send(f"\nBienvenido {user}.\n".encode())
                    else:
                        client.send(f"\nError al crear el usuario, pruebe otra vez...\n".encode("utf-8"))

                # Si la respuesta es 2, entonces...
                elif response == "2":
                    # Se envia información al cliente 
                    client.send("\nIngrese su nombre de usuario: ".encode("utf-8"))
                    # Se recibe la información que ingreso el cliente
                    username = client.recv(1024).decode("utf-8")

                    # Se envia información al cliente
                    client.send("\nIngrese su contraseña: ".encode("utf-8"))
                    # Se recibe la información que ingreso el cliente
                    password = client.recv(1024).decode("utf-8")
                    
                    # Si esta autenticado, entonces...
                    if self.authenticate(username, password):
                        user = username
                        client.send(f"\nBienvenido {user}.\n".encode("utf-8"))
                    # Si no..
                    else:
                        client.send("\nUsuario o contraseña incorrectos.\n".encode("utf-8"))

                # Si la respuesta es 3, entonces...
                elif parts[0] == "3":
                    # Se agarra los elementos correspondientes del array que tienen un valor.
                    user_to_send = parts[1].strip()
                    message_to_send = " ".join(parts[2:])
                    # Se llama a la función que permite enviar mensajes a usuarios.
                    self.send_msg_to_user(message_to_send, user, user_to_send)

                # Si la respuesta es 4, entonces...
                elif response == "4":
                    client.send("\n🟢 - Usuarios en linea:".encode("utf-8"))
                    # Se llama a la función .users_online()
                    online_users = self.users_online()
                    # Se envia la información de los usuarios conectados.
                    client.send(online_users.encode())

                # Si la respuesta es 5, entonces...
                elif response == "5":
                    # Se envia información al cliente
                    client.send("Escriba su mensaje para todos".encode())
                    # Se recibe la información que ingreso el cliente
                    message_from_client = client.recv(1024).decode()
                    # Llamado de la función que permite enviar mensajes a todos
                    self.send_msg_to_all_users_online(message_from_client, user)

                # Si la respuesta es 7, entonces..
                elif response == "6":
                    # Se envia información al cliente
                    client.send("Cerrando sesión...\n".encode())
                    # Se llama a la función correspondiente para desconectar a los usuarios.
                    self.disconnect(user)
                    break

        except Exception as error:
            print(f"Ocurrio un error a: {error}")
        except KeyboardInterrupt as error:
            print(f"Desconexion por parte del cliente")
            self.shutdown_socket()
            
    def start(self):
        """
        Esta función permite poner en funcionamiento el servidor,
        este utiliza hilos para manejar la conversación con los diferentes usuarios que se vayan conectando.
        """
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
                threading.Thread(target=self.conversation_with_client, args=(client, address, )).start()

        except Exception as error:
            print(f"Ocurrio un error al configurar el socket: {error}")
            self.shutdown_socket()
        except KeyboardInterrupt as error:
            print(f"Servidor apagado")
            self.shutdown_socket()

server = Server()
server.start()
