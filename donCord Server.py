import socket
import threading
import colorama
import time
from colorama import Fore, Back, Style


HOST = 'localhost'
PORT = 4990 #Port should be between 1024-9999 for non-root users
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

message = ""
users = {}  # Dictornary to store (username, client_socket)


def start():  # Creates Socket and Listens for Connections
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Searches for IPV4 connections
    serverSocket.bind(ADDRESS)
    serverSocket.listen(5)
    print("Server is searching for connections...")
    try:
        while True:
            client, addr = serverSocket.accept()
            print(f"{Fore.YELLOW}Connected With: {addr}")
            print(Style.RESET_ALL) #Resets text style
            
            username = client.recv(BUFSIZE).decode()
            users[username] = client  # Store the username and client socket
            print(f'{Style.BRIGHT}Connected Users: {list(users.keys())}') #Shows Users Connected On Dictionary
            client.send(f'Number of Connected Users: {len(users)}'.encode())

            
            connectionMessage = (f'{Fore.GREEN}---{username} connected---{Style.RESET_ALL}')
            chatSend(connectionMessage, client) #Sends Client Connected Message To Other Clients
            
            print(f'{Fore.CYAN}---Number of Connected Clients: {len(users)}---') #Server Logs Number Of Connections
            print(Style.RESET_ALL) #Resets text style

            # Start threads for reading and sending messages
            clientRead = threading.Thread(target=chatRead, args=(client, username)) #Makes Reading Thread
            clientRead.start() #Starts Reading Thread

    # WHEN CTRL+C IS PRESSED
    except KeyboardInterrupt: 
        print(f'{Fore.RED}Server Shutting Down...{Style.RESET_ALL}')
        client.send(f'{Fore.RED}Server is Shutting Down...'.encode())
        time.sleep(3)
        

    #Server Disconnect Message
    finally: 
        for uname,c in users.items(): # For All Clients in Server
            try:
                c.shutdown(socket.SHUT_RDWR)  # <- force-close the socket
                c.close()
            except:
                pass #Ignores All Errors
            
        serverSocket.close()
        print(f'{Fore.RED}Server Socket Closed...{Style.RESET_ALL}')



def remove_user(username, client): #Removes Users 
    global users
    disconnectionMessage =(f'{Fore.RED}---{username} has disconnected---{Style.RESET_ALL}') 
    print(disconnectionMessage)
    chatSend(disconnectionMessage, None) #Sends Disconnection Message To Other Clients
    print(Style.RESET_ALL) #Resets text style
    client.close()
    users.pop(username, None) #Removes Client From Users Dictonary
    print(f'---Current Users: {list(users.keys())}---')
                    
def chatSend(message, senderClient):  # Sends to All Clients Except Sender
    for uname, client in users.items():  # Use .items() to unpack key-value pairs
        if client != senderClient:
            client.send(message.encode())
    
            
def chatRead(client, username):  # Server Log, Reads Messages from Client
    while True:
        try:
            message = client.recv(BUFSIZE).decode()
            if not message:
                break
            if message == "/left":
                remove_user(username,client)
                break
            print(f'{username}: {message}')
            chatSend(f'{username}: {message}', client)

        except:
            remove_user(username, client)
            break



def main():
    start()

main()
