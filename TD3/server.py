import sys
import socket
import select

# get local machine name

host = socket.gethostname()

socketlist = []
recvbuffer = 2048
port = 6666

def chat_server():
    
# create a socket object

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind to the port

    serversocket.bind((host, port))

    # queue up to 5 requests

    serversocket.listen(5)

    socketlist.append(serversocket)

    while True:
        ready_to_read, ready_to_write, in_error = select.select(socketlist, [], [], 0)

        for sock in ready_to_read:
            if sock == serversocket:
                
                # establish a connection

                clientsocket, addr = serversocket.accept()
                
                socketlist.append(clientsocket)

                print("Connection de client avec IP %s" % str(addr))

                broadcast(serversocket, clientsocket, "[%s:%s] est entre dans le salon de discussion\n" % addr)
            else:
                try:
                    data = sock.recv(recvbuffer)
                    if data:
                        broadcast(serversocket, sock, "\r" + '[' + str(sock.getpeername()) + ']' + data)
                    else:
                        if sock in socketlist:
                            socketlist.remove(sock)
                            
                        broadcast(serversocket, sock, "Client (%s, %s) a quitte la salle\n" % addr)
                        
                except:
                    broadcast(serversocket, sock, "Client (%s, %s) a quitte la salle\n" % addr)
                    continue
                
        clientsocket.close()

    serversocket.close()

def broadcast(serversocket, sock, message):
    for socket in socketlist:
        if socket != serversocket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in socketlist:
                    socketlist.remove(socket)

if _name_ == "close":
    sys.exit(chat_server())
