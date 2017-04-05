import sys
import socket
import select

def chat_client():

    # create a socket object

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)

    # get local machine name

    host = socket.gethostname()

    port = 6666

    try:
        # connection to hostname on the port.
        
        s.connect((host, port))
        
    except:
        print "On ne peut pas se connecter"
        sys.exit()


    print "Connecte. Vous pouvez envoyer des messages"
    sys.stdout.write('<Moi>'); sys.stdout.fush()

    while True:
        socketlist = [sys.stdin, s]
        ready_to_read, ready_to_write, in_error = select.select(socketlist, [], [])

        for sock in ready_to_read:
            if sock == s:
                
                # Receive no more than 1024 bytes

                tm = s.recv(1024)

                if not tm:
                    print "\nDeconnecte du serveur"
                    sys.exit()
                else:
                    sys.stdout.write(tm)
                    sys.stdout.write('<Moi>'); sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('<Moi>'); sys.stdout.flush()



if _name_ == "close":
    sys.exit(chat_client())
    
