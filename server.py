import socket
from threading import Thread
import sys


if len(sys.argv) != 3: # if command line arguments arent sufficient port and host set to default
    sys.stdout.write("Not enough details given. Host and port set to default.")
    host = '0.0.0.0' # default host
    port = 8080 # default port
else:
    host = sys.argv[1] # given in command line
    port = int(sys.argv[2]) # given in command line

address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating an INET streaming socket
server_socket.bind(address) #  binds to a port to recieve connections takes host and port


clients = {} # clients dictionary with addresses : username

current_users = []

client_addresses = {} # clients client_addresses 
users_online = 0 # number of users online

def connections(): # function that handles clients that are trying to connected
    
    server_socket.listen(5)

    print ("\n------------------- Server opened on port " + str(port) + "-------------------\n")

    while True:

        client, client_address = server_socket.accept()

        sys.stdout.write(str(client_address) + " connected.\n")
        sys.stdout.flush() # printing immediately into the terminal



        client.send("Welcome to the chatroom!\n  Enter your name.".encode())

        client_addresses[client] = client_address

        Thread(target=active_clients, args=(client,)).start()


def active_clients(client):  

    global users_online # gloabal users online

    name = client.recv(1024).decode() # clients name

    users_online += 1

    welcome = "Welcome " + name + "\n Type {quit} to exit."

    client.send(welcome.encode())

    user_online = "---------- You haved joined the chat. " + str(users_online) + " users online----------"

    client.send(user_online.encode()) # sending to just the user who has joined the chat

    total = "---------- Currently " + str(users_online) + " user(s) online----------" 

    broadcast(total.encode()) # sent to all users in the chat to know that someone has joined + new current total

    data = "*** " + name + " has entered the chat. ***" 

    broadcast(data.encode()) # sending to everyone in chat that a new person has joined

    clients[client] = name # adding client address etc and users name into a dictionary
    


    while True:

        data = client.recv(1024)

        if data != "{quit}".encode(): # if data doesnt equal to quit

            broadcast(data, name + ": ") # print data


        else:

            client.send("{quit}".encode()) # client sends {quit}

            client.close() # close the client connection

            del clients[client] # delete the client from the dictionary

            broadcast((name + "has disconnected.").encode()) # broadcasted to all clients currently in the server that use rhas disconnected

            break


def broadcast(data, name=""):  # this function broadcasts message to all active clients

    for sock in clients:
        sock.send(name.encode() + data )

        

if __name__ == "__main__":



    print("Waiting for connections.\n")

    start = Thread(target=connections) # initialising thread

    start.start() # starts the thread

    start.join() # terminating start threads
    print(clients)

    server_socket.close()