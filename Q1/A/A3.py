# 816016584
"""
This program generates an HMAC for the Binary data (Letter) and send it to
program B3.
"""
import hmac
from hashlib import sha256
from binascii import unhexlify
from socket import socket, gethostname

LetterBinary = "LetterBinary"  # Location of the stored Binary (ascii) converted Letter
aesFile = "AESKeyFile"  # Location of the aes symmeteric key
PORT = 34456  # Port used in program A3 and B3


def readFile(relativeFilePathAndName):
    #  Reads a given ".dat" file and returns its data.
    try:
        with open(f"{relativeFilePathAndName}.dat", "r") as f:
            data = f.read()
            if data:
                return data
            else:  # If there is no data in the file
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
    # Listen until a client is available, and establish a TCP connection and return socket object
    print("Listening to connection")
    sock.listen(1)
    client, clientAddress = sock.accept()
    print("client connected.")
    return client


def sendHmac(hmac):
    # This function converts hmac object to a hexadecimal digest and send it to bob
    digest = hmac.hexdigest()
    sock = makeServer()
    conn = listenForConnection(sock)
    sendData(digest, conn)


if __name__ == "__main__":
    key = readFile(aesFile)  # Get symmetric key
    message = readFile(LetterBinary)
    # Generate hmac using SYmmetric key, message and sha256 algorithm
    hmac = hmac.new(unhexlify(key), message.encode(), sha256)
    sendHmac(hmac)
