import socket
import threading
import colorama
from colorama import Fore, Back, Style

HOST = 'localhost'
PORT = 4998
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
loginFile = "logins.txt"
users = {}  # Dictionary to store (username, client_socket)

message = ""

def loadLogin(): # Loads The Login Text File
    login = {}
    try:
        file = open(loginFile, "r")
        for line in file:
            username, password = line.strip().split(",")
            login[username] = password # login[username] returns password
        file.close()
    except FileNotFoundError:
        print("Login file not found. A new one will be created.")
    except Exception as e: # For any other error
        print(f"An error occurred: {e}")
    return login


def saveLogin(username, password): # Saves A Username And Password Pair
    file = open(loginFile, "a") # a = append | adds text to file instead of overwriting the entire file. 
    file.write(f'{username},{password}\n')
    file.close()
    return(f'Saved Login: ')
    
def loginClient(client):
    login = loadLogin()
    while True:
        client.send("Enter Your Username: ".encode())
        username = client.recv(BUFSIZE).decode().strip() # Strip = Removes any blank spaces and just takes text
        client.send("Enter Your Password: ".encode())
        password = client.recv(BUFSIZE).decode().strip()
        
        
        if username in login:
            if login[username] == password:  # logins[username] returns password
                client.send(f'{Fore.GREEN}Login Successful!'.encode())
                return username
            else:
                print("Incorrect Login. Try Again.")
                client.send("Incorrect password. Try again.".encode())
        else:
            client.send(f'{Fore.YELLOW}Username not found, would you like to create an account (yes/no):  '.encode())
            print(Style.RESET_ALL)
            response = client.recv(BUFSIZE).decode().strip()
            if response.lower() == "yes" or response.lower() == "y":
                saveLogin(username, password)
                client.send(f'{Fore.GREEN}Registration Success. You are now logged in.'.encode())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                print(Style.RESET_ALL)
                print(f'{Fore.CYAN}--NEW ACCOUNT CREATED--')
                print(Style.RESET_ALL)
                return username  # Proceed with logged-in user after registration
            else: # NO
                client.send(f'{Fore.RED}Login Failed, Try Again...'.encode())
                continue  # Allow the user to try logging in again

def start():  # Creates Socket and Listens for Connections
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Searches for IPV4 connections
    serverSocket.bind(ADDRESS)
    serverSocket.listen(5)
    print("Server is searching for connections...")
    
    while True:
        client, addr = serverSocket.accept()
        print(f"{Fore.GREEN}Connected With: {addr}")
        print(Style.RESET_ALL)
        
        try:
            username = loginClient(client)  # Username for other clients
            users[username] = client  # Store the username and client socket
            print(f'Connected Users: {list(users.keys())}')  # Shows Users Connected on Dictionary
            client.send(f'{Fore.CYAN}---Number Of Users Online: {len(users)}---'.encode())

            connectionMessage = (f'{Fore.GREEN}---{username} Connected---')
            print(Style.RESET_ALL)
            chatSend(connectionMessage, client)  # Sends Client Connected Message To Other Clients

            print(f'{Fore.CYAN}---Number of Connected Clients: {len(users)}---')  # Server Logs Number Of Connections
            print(Style.RESET_ALL)

            # Start threads for reading and sending messages
            clientRead = threading.Thread(target=chatRead, args=(client, username))  # Makes Reading Thread
            clientRead.start()  # Starts Reading Thread
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            client.close()

def remove_user(username, client): # Removes Users 
    global users
    disconnectionMessage =(f'{Fore.RED}---{username} has Disconnected---') 
    print(disconnectionMessage)
    chatSend(disconnectionMessage, None)  # Sends Disconnection Message To Other Clients
    print(Style.RESET_ALL)  # Resets text style
    client.close()
    users.pop(username, None)  # Removes Client From Users Dictionary
    print(f'---Current Users: {list(users.keys())}---')

def chatSend(message, senderClient):  # Sends to All Clients Except Sender
    for uname, client in users.items():  # Use .items() to unpack key-value pairs
        if client != senderClient:
            try:
                client.send(message.encode())
            except:
                pass

def chatRead(client, username):  # Server Log / Reads Messages from Client
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
    logins = loadLogin()
    print("Loaded Logins:", logins)
    start()

main()
