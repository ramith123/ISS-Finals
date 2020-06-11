from socket import socket, gethostname


port = 12345


def ClientsendMessage(message, sock):
    # Send a server given message thorugh given socket
    try:
        print("Sending message...")
        sock.sendall(message)
        print("Message sent, Closing Connection.")
        sock.close()
    except:
        print("Connection Error. Aborting")
        exit()


def connectToServer():
    sock = socket()
    try:
        sock.connect((gethostname(), port))
    except ConnectionRefusedError:
        print("Server Unavailable")
    print("Server Connection successfull.")
    return sock


print("Heelow world")
