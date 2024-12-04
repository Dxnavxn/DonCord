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
    userName = input(">").lower()
    clientSocket.send(userName.encode())

    print(clientSocket.recv(BUFSIZE).decode())
    password = input(">")
    clientSocket.send(password.encode())


    loginResponse =clientSocket.recv(BUFSIZE).decode()
    if "Successful" in loginResponse:
        print(f'{Fore.GREEN}---Login Successful---')
        print(Style.RESET_ALL)
        print(f'{Fore.BLUE}>>Welcome To DonCord, {userName}<<')
        print(Style.RESET_ALL)
        print(clientSocket.recv(BUFSIZE).decode())
        print(Style.RESET_ALL)
        return userName
    else:
        print(f'{Fore.YELLOW}No Account Found...')
        print(Style.RESET_ALL)


        
    if "would you like to create an account " in loginResponse:
        createAccount = input("Do you want to create a new account (Yes/No): ").strip().lower()

        if createAccount.lower() == "yes" or createAccount.lower() == "y":
            clientSocket.send("yes".encode()) #fake yes
        
            loginResponse = clientSocket.recv(BUFSIZE).decode() # Account creation success message
            print(loginResponse)
            print(f'{Fore.BLUE}>>Welcome To DonCord, {userName}<<')
            print(Style.RESET_ALL)
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