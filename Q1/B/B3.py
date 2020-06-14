"""
This program receives HMAC from Alice, generate its own HMAC using Symmetric key and message, then compares the two
to detect integrity anomalies and authenticate sent user.
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


def connectToServer():
    # This function establishes a connection with a server. The function works on the same host and use the PORT number to look for a server
    sock = socket()
    try:
        sock.connect((gethostname(), PORT))  # Connects to local host and specified host
        print("Server Connection successfull.")
        return sock  # returns a socket object when a connection is successful
    except ConnectionRefusedError:
        print(f"Server Unavailable. Make sure the server is running on port {PORT} ")
        exit()


def receiveDataFromConnection(connection):
    # This function receives data from a given socket.
    message = ""
    try:
        print("Trying to receive msg.")
        data = connection.recv(1024).decode()
        while data:  # In order to get data that is larger than 1024 bits
            message += data
            if len(data) < 1024:  # break the loop if the data is less than 1024
                break
            data = connection.recv(1024).decode()
        print("Message received.")
        return message
    except ConnectionError:
        print("Connection error")
        connection.close()
        exit()


def recieveHmac():
    # Get Hmac from alice's Server
    sock = connectToServer()
    hmac = receiveDataFromConnection(sock)
    return hmac


def compareHmac(newh, oldh):
    # compare alices Hmac with This programs generated Hmac
    newh = newh.hexdigest()
    return newh == oldh


if __name__ == "__main__":

    key = readFile(aesFile)  # Get symmetric key
    message = readFile(LetterBinary)
    # Generate hmac using SYmmetric key, message and sha256 algorithm
    newh = hmac.new(unhexlify(key), message.encode(), sha256)
    # Get Hmac from alice
    oldh = recieveHmac()

    # Comparison result
    if compareHmac(newh, oldh):

        print("This message came from A, And has not been altered.")
    else:
        print(
            "Something was wrong with this message. Might be altered or A didn't send it"
        )
