import socket
import threading
import colorama
from colorama import Fore, Back, Style
import sys

#INIT
HOST = 'localhost'
PORT = 4992
BUFSIZE = 1024
ADDRESS =(HOST,PORT)


clientSocket = socket.socket()
clientSocket.connect(ADDRESS)

usernamePrompt = input(f'{Fore.CYAN}{Style.BRIGHT}Enter a Username: ')
clientSocket.send(usernamePrompt.encode())
print(Style.RESET_ALL) #Resets text style

print(f'Welcome To DonCord, {usernamePrompt}')
print(clientSocket.recv(BUFSIZE).decode())



serverMessage = ""

def chatSend():
    while True:
        input_str = input(">> ")
        # Move cursor up one line, clear line
        sys.stdout.write('\033[F')   # move cursor up
        sys.stdout.write('\033[K')   # clear line
        sys.stdout.flush()
        clientSocket.send(input_str.encode())
        print(f'YOU: {input_str}')

        
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