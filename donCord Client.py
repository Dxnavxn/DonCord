import socket
import threading
import colorama
from colorama import Fore, Back, Style


#INIT
HOST = 'localhost'
PORT = 5000
BUFSIZE = 1024
ADDRESS =(HOST,PORT)


clientSocket = socket.socket()
clientSocket.connect(ADDRESS)

print(clientSocket.recv(BUFSIZE).decode())
userName = input(">")

clientSocket.send(userName.encode())
print(f'Welcome To DonCord, {userName}')
print(clientSocket.recv(BUFSIZE).decode())



serverMessage = ""

def chatSend():
    while True:
        message = input(">>")
        clientSocket.send((f'{message}').encode())
        
def chatRead():
    global serverMessage
    while True:
            serverMessage = clientSocket.recv(BUFSIZE).decode()
            print(serverMessage)
            print(Style.RESET_ALL)

        

        
chatThread = threading.Thread(target=chatSend)
readThread = threading.Thread(target=chatRead)

chatThread.start()
readThread.start()

chatThread.join()
readThread.join()