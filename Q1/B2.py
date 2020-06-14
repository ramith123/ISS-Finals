from hashlib import sha256
from Crypto.Cipher import DES
from socket import socket, gethostname
import time

p = 7
g = 5
bSecretNumber = 593
PORT = 7892


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


def receiveDataFromConnection(connection):
    message = ""
    try:
        print("Trying to receive msg.")
        data = connection.recv(1024).decode()
        while data:
            message += data
            if len(data) <= 1024:
                break
            data = connection.recv(1024).decode()
        print("Message received.")
        return message
    except ConnectionError:
        print("Connection error")
        connection.close()
        exit()


def sendData(message, sock):
    # Send a server given message thorugh given socket
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")

    except:
        print("Connection Error. Aborting")
        exit()


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def generatePublicKey():
    return (g ** bSecretNumber) % p


def generateSharedKey(bSharableKey):
    key = (bSharableKey ** bSecretNumber) % p
    hashkey = sha256(str(key).encode())
    return hashkey.hexdigest()


def sendPublicKey(connection):
    key = generatePublicKey()
    sendData(str(key), connection)


def getPublicKey(connection):
    key = receiveDataFromConnection(connection)
    return int(key)


def diffHelExchangeServer():
    sock = makeServer()
    connection = listenForConnection(sock)
    sendPublicKey(connection)
    akey = getPublicKey(connection)
    connection.close()
    return akey


if __name__ == "__main__":
    print(diffHelExchangeServer())
