from socket import gethostname, socket

port = 1245


def makeServer():
    sock = socket()
    sock.bind((gethostname(), port))
    print("Server socket setup complete")
    return sock


def listenForConnection(sock):
    print("Listening to connection")
    sock.listen(1)
    client, clientAddress = sock.accept()
    print("client connected.")
    return client


def receiveData(client):
    message = ""
    try:
        print("Trying to receive msg.")
        data = client.recv(1024).decode()
        while data:
            message += data
            data = client.recv(1024).decode()
        print("Message received.")
        return message
    except ConnectionError:
        print("Connection error")
        client.close()
        exit()


def nameLater():
    sock = makeServer()
    conn = listenForConnection(sock)
    print(receiveData(conn))
    conn.close()


if __name__ == "__main__":
    nameLater()
