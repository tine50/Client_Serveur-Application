# server.py
import socket
import threading

clients = {}  # Dictionnaire pour stocker le socket et le nom d'utilisateur

def broadcast_message(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:  # Envoyer le message aux autres clients uniquement
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket):
    try:
        # Le premier message reçu est le nom d'utilisateur
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} s'est connecté.")
        broadcast_message(f"{username} a rejoint le chat.", client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{username}: {message}")
            broadcast_message(f"{message}", client_socket)
    except:
        pass
    finally:
        client_socket.close()
        del clients[client_socket]
        broadcast_message(f"{username} a quitté le chat.", client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Remplacer par l'adresse IP et le port désiré
    server_socket.listen(5)
    print("Serveur en attente de connexions...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion établie avec {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
