import hmac
from hashlib import sha256
from binascii import unhexlify
from socket import socket, gethostname

LetterBinary = "LetterBinary"
aesFile = "AESKeyFile"
PORT = 34456


def readFile(relativeFilePathAndName):
    try:
        with open(f"{relativeFilePathAndName}.dat", "r") as f:
            data = f.read()
            if data:
                return data
            else:
                raise Exception(f"No data in {relativeFilePathAndName}.dat file")
                exit()
    except FileNotFoundError:
        print(f"File called {relativeFilePathAndName}.dat is not found")
        exit()


def connectToServer():
    sock = socket()
    try:
        sock.connect((gethostname(), PORT))
        print("Server Connection successfull.")
        return sock
    except ConnectionRefusedError:
        print(f"Server Unavailable. Make sure the server is running on port {PORT} ")
        exit()


def receiveDataFromConnection(connection):
    message = ""
    try:
        print("Trying to receive msg.")
        data = connection.recv(1024).decode()
        while data:
            message += data
            if len(data) < 1024:
                break
            data = connection.recv(1024).decode()
        print("Message received.")
        return message
    except ConnectionError:
        print("Connection error")
        connection.close()
        exit()


def recieveHmac():
    sock = connectToServer()
    hmac = receiveDataFromConnection(sock)
    return hmac


def compareHmac(newh, oldh):
    newh = newh.hexdigest()
    return newh == oldh


if __name__ == "__main__":
    key = readFile(aesFile)
    message = readFile(LetterBinary)
    newh = hmac.new(unhexlify(key), message.encode(), sha256)
    oldh = recieveHmac()
    if compareHmac(newh, oldh):

        print("This message came from A, And has not been altered.")
    else:
        print(
            "Something was wrong with this message. Might be altered or A didn't send it"
        )
