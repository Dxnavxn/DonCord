import socket
import threading
import colorama
from colorama import Fore, Back, Style


HOST = 'localhost'
PORT = 499 # Port should be between 1024-9999 for non-root users
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

message = ""
users = {}  # Dictornary to store (username, client_socket)


def start():  # Creates Socket and Listens for Connections
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Searches for IPV4 connections
    serverSocket.bind(ADDRESS)
    serverSocket.listen(5)
    print("Server is searching for connections...")
    
    while True:
        client, addr = serverSocket.accept()
        print(f"{Fore.YELLOW}Connected With: {addr}")
        print(Style.RESET_ALL) #Resets text style
        
        username = client.recv(BUFSIZE).decode()
        users[username] = client  # Store the username and client socket
        print(f'{Style.BRIGHT}Connected Users: {list(users.keys())}') #Shows Users Connected On Dictionary
        client.send(f'Number of Connected Users: {len(users)}'.encode())

        
        connectionMessage = (f'{Fore.GREEN}---{username} connected---')
        print(Style.RESET_ALL) #Resets text style
        chatSend(connectionMessage, client) #Sends Client Connected Message To Other Clients
        
        print(f'{Fore.CYAN}---Number of Connected Clients: {len(users)}---') #Server Logs Number Of Connections
        print(Style.RESET_ALL) #Resets text style

        # Start threads for reading and sending messages
        clientRead = threading.Thread(target=chatRead, args=(client, username)) #Makes Reading Thread
        clientRead.start() #Starts Reading Thread
        
def remove_user(username, client): #Removes Users 
    global users
    disconnectionMessage =(f'{Fore.RED}---{username} has disconnected---') 
    print(disconnectionMessage)
    chatSend(disconnectionMessage, None) #Sends Disconnection Message To Other Clients
    print(Style.RESET_ALL) #Resets text style
    client.close()
    users.pop(username, None) #Removes Client From Users Dictonary
    print(f'---Current Users: {list(users.keys())}---')
                    
def chatSend(message, senderClient):  # Sends to All Clients Except Sender
    for uname, client in users.items():  # Use .items() to unpack key-value pairs
        if client != senderClient:
            try:
                client.send(message.encode())
            except:
                print(f"Failed to send message to {uname}")
            
def chatRead(client, username):  # Server Log, Reads Messages from Client
    global message
    while True:
        try:
            message = client.recv(BUFSIZE).decode()
            if message:
                print(f"{username}: {message}")
                chatSend(f"{username}: {message}", client)
        except:
            print(f"{username} has disconnected.")
            remove_user(username, client)
            break

def main():
    start()

main()
