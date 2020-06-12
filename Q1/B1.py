from socket import gethostname, socket

PORT = 1245


def makeServer():
    # Creates a server on port specified. returns the socket object.
    sock = socket()
    sock.bind((gethostname(), PORT))
    print("Server socket setup complete")
    return sock


def listenForConnection(sock):
    print("Listening to connection")
    sock.listen(1)
    client, clientAddress = sock.accept()
    print("client connected.")
    return client


def receiveData(sock):
    message = ""
    try:
        print("Trying to receive msg.")
        data = sock.recv(1024).decode()
        while data:
            message += data
            data = sock.recv(1024).decode()
        print("Message received.")
        return message
    except ConnectionError:
        print("Connection error")
        sock.close()
        exit()


def nameLater():
    sock = makeServer()
    conn = listenForConnection(sock)
    print(receiveData(conn))
    conn.close()
