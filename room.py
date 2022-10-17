# Assignment 2
# Maya Michalik
# room.py server side

import argparse
import signal
from socket import *

# Terminates program if Ctrl-C is entered
def handler(sig, frame):
    exit(1)
 
signal.signal(signal.SIGINT, handler)


parser = argparse.ArgumentParser(description="Room Starting Description: ")

# comand line arguments
parser.add_argument('port', help="The port number that the server will wait for client messages on.", type = int)
parser.add_argument('name', help="The name of the room running on the server.", type = str)
parser.add_argument('description', help="A textual description of the room", type = str)
parser.add_argument('items', help="A list of items to be found in the room initally", nargs='+')
args = parser.parse_args()


serverPort = args.port
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))

# prints description, room name, and list of items
print(parser.description)
print(args.name)
print(args.description)
print("In this room, there is: ")

i=0
for i in range(len(args.items)):
    print(args.items[i])
    i+=i

print("Room will wait for players at port: "+ str(args.port))

# prints when player joins server
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decodeMsg = message.decode()
    print(decodeMsg)
    break

# sends necessary information to player
retMsg = args.description + ' \n '

while True:
    retMsg += "In this room, there is: \n "

    i=0
    for i in range(len(args.items)):
        retMsg += args.items[i]+ ' \n '
        i+=i  
    serverSocket.sendto(retMsg.encode(), clientAddress)
    break

PlayerInventory =[]
clientReq = ['look', 'take', 'drop', 'inventory']

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decodeMsg = message.decode()

    # if user entered look
    if decodeMsg.lower() == clientReq[0]:
        retMsg = args.name
        serverSocket.sendto(retMsg.encode(), clientAddress)
    
    # if user entered take "item"
    if decodeMsg.lower()[:4] == clientReq[1]:
        taken = False

        # if item in the item list
        for i in args.items[:]:
            if decodeMsg.lower() == clientReq[1]+ " " + i:
                
                # remove it from room and add it to inventory
                (args.items).remove(i)
                PlayerInventory.append(i)

                retMsg = i + " taken"
                serverSocket.sendto(retMsg.encode(), clientAddress)
                taken =True
        # else say item cannot be taken
        if taken == False:
            retMsg = "You cannot take that."
            serverSocket.sendto(retMsg.encode(), clientAddress)
        

    # if user entered drop item
    elif decodeMsg.lower()[:4] == clientReq[2]:
        
        dropped = False
        # if item in inventory
        for i in PlayerInventory[:]:
            if decodeMsg.lower() == clientReq[2]+ " " + i:

                # remove from inventory and add it back to room
                (PlayerInventory).remove(i)
                (args.items).append(i)

                retMsg = i + " Dropped"
                serverSocket.sendto(retMsg.encode(), clientAddress)
                dropped = True
        # else say item cannot be dropped
        if dropped == False:
            retMsg = "You are not holding that."
            serverSocket.sendto(retMsg.encode(), clientAddress)


    # if user entered inventory
    elif decodeMsg.lower() == clientReq[3]:
        
        # if inventory has items send mesg to player
        if len(PlayerInventory) >= 1:
            retMsg = "You are holding:\n" 

            for p in PlayerInventory[:]:
                retMsg+= p + "\n"
        else:
            retMsg = "You are not holding anything." 

        serverSocket.sendto(retMsg.encode(), clientAddress)

    # if user enters inccorect input
    else:
        retMsg = "invalid input"
        serverSocket.sendto(retMsg.encode(), clientAddress)
