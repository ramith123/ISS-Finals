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


def sendData(message, sock):
    # Send a server given message thorugh given socket
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")

    except:
        print("Connection Error. Aborting")
        exit()


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


def sendHmac(hmac):
    digest = hmac.hexdigest()
    sock = makeServer()
    conn = listenForConnection(sock)
    sendData(digest, conn)


if __name__ == "__main__":
    key = readFile(aesFile)
    message = readFile(LetterBinary)
    hmac = hmac.new(unhexlify(key), message.encode(), sha256)
    sendHmac(hmac)
