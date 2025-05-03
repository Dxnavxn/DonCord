import socket
import threading
import colorama
from colorama import Fore, Back, Style
import sys
import os

#INIT
HOST = 'localhost'
PORT = 4991
BUFSIZE = 1024
ADDRESS =(HOST,PORT)


clientSocket = socket.socket()
clientSocket.connect(ADDRESS)

usernamePrompt = input(f'{Fore.CYAN}{Style.BRIGHT}Enter a Username: ')
clientSocket.send(usernamePrompt.encode())
print(Style.RESET_ALL) #Resets text style

print(f'Welcome To DonCord, {usernamePrompt}')
print(clientSocket.recv(BUFSIZE).decode())




def chatSend():
    global serverMessage
    while True:
        try:
            inputStr = input(">>")
            sys.stdout.write('\033[F')   # move cursor up
            sys.stdout.write('\033[K')   # clear line
            sys.stdout.flush()
            clientSocket.send(inputStr.encode())
            print(f'YOU: {inputStr}')

        except:
             break
        
def chatRead():
    global serverMessage
    clientSocket.settimeout(1.0)
    while True:
            try:
                serverMessage = clientSocket.recv(BUFSIZE).decode()
                if not serverMessage:
                     print(f'{Fore.RED}\nServer Disconnected...{Style.RESET_ALL}')
                     break
                
                sys.stdout.write('\r')   # move to start of line
                sys.stdout.write('\033[K')   # clear line

                sys.stdout.write(f'{serverMessage}\n')
                sys.stdout.write(">> ")
                sys.stdout.flush()
            except socket.timeout:
                 continue
            except:
                 break
    os._exit(0)
        

        
chatThread = threading.Thread(target=chatSend)
readThread = threading.Thread(target=chatRead)

chatThread.start()
readThread.start()

try:
    chatThread.join()
    readThread.join()

except KeyboardInterrupt: #When Pressing Cntrl + C
     print(f'{Fore.RED}Leaving DonCord...')
     clientSocket.send(b"/left")
     clientSocket.close()
     os._exit
