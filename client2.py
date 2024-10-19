import socket  # Module pour créer des connexions réseau
import threading  # Module pour gérer les threads
import tkinter as tk  # Module pour créer l'interface graphique
from tkinter import scrolledtext, simpledialog  # Importation de widgets Tkinter

class ChatClient:
    def __init__(self, master, title):
        # Initialisation de la classe ChatClient
        self.master = master  # Référence à la fenêtre principale
        self.master.title(title)  # Définition du titre de la fenêtre

        # Interface graphique
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled')
        # Zone de texte défilante pour afficher les messages de chat
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Définir les balises pour l'alignement et les couleurs d'arrière-plan des messages
        self.chat_area.tag_configure("left", justify="left", background="lightblue")  # Messages reçus
        self.chat_area.tag_configure("right", justify="right", background="lightgreen")  # Messages envoyés

        # Champ de saisie pour les messages
        self.message_entry = tk.Entry(self.master, width=50)
        self.message_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)  # Écoute l'appui sur "Entrée" pour envoyer le message

        # Bouton pour envoyer le message
        self.send_button = tk.Button(self.master, text="Envoyer", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)

        # Connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Création du socket
        self.client_socket.connect(('127.0.0.1', 12345))  # Connexion à l'adresse IP et au port du serveur

        # Demander le nom d'utilisateur
        self.username = simpledialog.askstring("Nom d'utilisateur", "Entrez votre nom d'utilisateur", parent=self.master)
        # Si l'utilisateur ne saisit pas de nom, utiliser "Anonyme" par défaut
        if not self.username:
            self.username = "Anonyme"

        # Mettre à jour le titre de la fenêtre avec le nom d'utilisateur
        self.master.title(f"Chat - {self.username}")

        # Envoyer le nom d'utilisateur au serveur
        self.client_socket.send(self.username.encode('utf-8'))

        # Démarrer un thread pour recevoir les messages
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, event=None):
        # Fonction pour envoyer un message
        message = self.message_entry.get()  # Récupérer le message dans le champ de saisie
        if message:  # Si le message n'est pas vide
            # Format du message : "envoyeur: message"
            full_message = f"{self.username}: {message}"
            self.client_socket.send(full_message.encode('utf-8'))  # Envoyer le message au serveur
            self.display_message(f"{self.username}: {message}", align="right", tag="right")  # Afficher le message dans la zone de chat
            self.message_entry.delete(0, tk.END)  # Effacer le champ de saisie

    def receive_messages(self):
        # Fonction pour recevoir les messages du serveur
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')  # Recevoir un message du serveur
                # Vérifier si le message n'a pas été envoyé par soi-même
                if not message.startswith(f"{self.username}:"):
                    self.display_message(message, align="left", tag="left")  # Afficher le message reçu dans la zone de chat
            except:
                break  # Sortir de la boucle si une erreur se produit

    def display_message(self, message, align="left", tag="left"):
        # Fonction pour afficher un message dans la zone de chat
        self.chat_area.config(state='normal')  # Permettre les modifications dans la zone de chat
        self.chat_area.insert(tk.END, f"{message}\n", tag)  # Insérer le message avec la balise spécifiée
        self.chat_area.yview(tk.END)  # Faire défiler vers le bas pour afficher le dernier message
        self.chat_area.config(state='disabled')  # Désactiver les modifications pour éviter que l'utilisateur ne puisse écrire ici

if __name__ == "__main__":
    root = tk.Tk()  # Créer la fenêtre principale
    app = ChatClient(root, "Client 2")  # Initialiser l'application avec le titre par défaut
    root.mainloop()  # Démarrer la boucle principale de l'interface graphique
