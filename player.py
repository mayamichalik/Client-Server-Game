# Assignment 2
# Maya Michalik
# player.py client side

import argparse
from urllib.parse import urlparse
import signal
from socket import *

# Terminates program if Ctrl-C is entered
def handler(sig, frame):
    exit(1)
 
signal.signal(signal.SIGINT, handler)

# comand line arguments
parser = argparse.ArgumentParser()
parser.add_argument('playername', help="The single-word name of the player in the game", type = str)
parser.add_argument('serverAddress', help="An address for the game server to message.", type = str)
args = parser.parse_args()

url = urlparse(args.serverAddress)

serverName = url.hostname
serverPort = url.port
clientSocket = socket(AF_INET, SOCK_DGRAM)

# sending name of player to server
while True:
    join = "User " + args.playername + " joined from address " + str(args.serverAddress)
    clientSocket.sendto(join.encode(), (serverName, serverPort))
    break

# loop until we receive message from client
while True:
    joinMsg, serverAddress = clientSocket.recvfrom(2048)
    if joinMsg:
        joinMsg = joinMsg.decode()
        joinMsg.replace('\\n','\n')
        print(joinMsg)
        break

message = ''
# loop if blanks input
while message =='':
    message = input(">")

# while user input is not exit
while message.lower().strip() != 'exit':

    # send and recieve messages to server
    clientSocket.sendto(message.encode(), (serverName, serverPort))
   
    msg, serverAddress = clientSocket.recvfrom(2048)
    msg = msg.decode()
    print(msg)
    
    message = ''
    while message =='':
        message = input(">")
    
clientSocket.sendto(message.encode(), (serverName, serverPort))
clientSocket.close()