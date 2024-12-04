import socket
import threading
import colorama
from colorama import Fore, Back, Style
from hashlib import sha256


#INIT
HOST = 'localhost'
PORT = 4998
BUFSIZE = 1024
ADDRESS =(HOST,PORT)


clientSocket = socket.socket()
clientSocket.connect(ADDRESS)

def login():
    print(clientSocket.recv(BUFSIZE).decode())
    userName = input(">")
    clientSocket.send(userName.encode())

    print(clientSocket.recv(BUFSIZE).decode())
    password = input(">")
    clientSocket.send(password.encode())


    loginResponse = clientSocket.recv(BUFSIZE).decode()
    if "Successful" in loginResponse:
        print(f'{Fore.GREEN}---Login Successful---')
        print(Style.RESET_ALL)
        print(f'{Fore.BLUE}>>Welcome To DonCord, {userName}<<')
        print(Style.RESET_ALL)
        print(clientSocket.recv(BUFSIZE).decode())
        print(Style.RESET_ALL)
        return userName

    elif "Trying Again.." in loginResponse:
        print(f'{Fore.RED}Incorrect Username or Password. Try Again')
        print(Style.RESET_ALL)
        
    elif "Username Already Taken." in loginResponse:
        print(f'{Fore.CYAN}Username already taken. Try Again..')
        print(Style.RESET_ALL)

        
    elif "would you like to create an account " in loginResponse:
        print(clientSocket.recv(BUFSIZE).decode())
        createAccount = input("Do you want to create a new account (Yes/No): ").strip().lower()

        if createAccount.lower() == "yes" or createAccount.lower() == "y":
            clientSocket.send("yes".encode()) #fake yes
        
            loginResponse = clientSocket.recv(BUFSIZE).decode() # Account creation success message
            print(loginResponse)
            return userName
        else:
            print(f'{Fore.RED}Login failed. Try again.')
            print(Style.RESET_ALL)
            clientSocket.close()
            exit()


def chatSend():
    while True:
        message = input(">>")
        clientSocket.send((f'{message}').encode())
        
def chatRead():
    while True:
            serverMessage = clientSocket.recv(BUFSIZE).decode()
            print(serverMessage)
            print(Style.RESET_ALL)

        

userName = login()

chatThread = threading.Thread(target=chatSend)
readThread = threading.Thread(target=chatRead)

chatThread.start()
readThread.start()

chatThread.join()
readThread.join()