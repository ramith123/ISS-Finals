from hashlib import sha256
from Crypto.Cipher import DES
from socket import socket, gethostname

p = 7
g = 5
aSecretNumber = 475
PORT = 7892


def connectToServer():
    sock = socket()
    try:
        sock.connect((gethostname(), PORT))
        print("Server Connection successfull.")
        return sock
    except ConnectionRefusedError:
        print(f"Server Unavailable. Make sure the server is running on port {PORT} ")
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


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def generatePublicKey():
    return (g ** aSecretNumber) % p


def generateSharedKey(bSharableKey):
    key = (bSharableKey ** aSecretNumber) % p
    hashkey = sha256(str(key).encode())
    return hashkey.hexdigest()


def sendPublicKey(connection):
    key = generatePublicKey()
    sendData(str(key), connection)


def getPublicKey(connection):
    key = receiveDataFromConnection(connection)
    return int(key)


def diffHelExchangeClient():
    conn = connectToServer()
    bkey = getPublicKey(conn)
    sendPublicKey(conn)

    conn.close()
    return bkey


if __name__ == "__main__":
    print(diffHelExchangeClient())
