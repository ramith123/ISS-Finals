from socket import socket, gethostname
import random
from textwrap import wrap

PORT = 1245
OTPNumberOfBits = 1000


def connectToServer():
    sock = socket()
    try:
        sock.connect((gethostname(), PORT))
        print("Server Connection successfull.")
        return sock
    except ConnectionRefusedError:
        print(f"Server Unavailable. make sure the port is {PORT}")
        exit()


def sendData(message, sock):
    # Send a server given message thorugh given socket
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")
        sock.close()
    except:
        print("Connection Error. Aborting")
        exit()


def generatBinaryFile(data, fileName, convert=True):
    if convert:
        data = bin(data)[2:]
    with open(f"{fileName}.dat", "w+") as f:
        f.write(data)


def generateOTPKeyFile():
    randomBits = random.getrandbits(OTPNumberOfBits)
    generatBinaryFile(randomBits, "OTPGeneratedKey")


def readFile(fileName):
    try:
        with open(f"{fileName}.dat", "r") as f:
            data = f.read()
            if data:
                return data
            else:
                raise Exception(f"No data in {fileName}.dat file")
    except FileNotFoundError:
        print(f"File called {fileName}.dat is not found")


def convertLetterToBinary():
    text = readFile("Letter")
    data = textToBinary(text)
    generatBinaryFile(data, "LetterBinary", False)


def textToBinary(text):
    data = "".join(f"{ord(i):08b}" for i in text)
    return data


def binaryToText(binary):
    array = wrap(binary, 8)
    array = [int(i, 2) for i in array]
    text = "".join(map(chr, array))
    return text


if __name__ == "__main__":
    pass
