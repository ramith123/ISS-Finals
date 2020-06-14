from socket import socket, gethostname
import random
from textwrap import wrap
from os import path

PORT = 1245
OTPNumberOfBits = 1000
LetterFile = "Letter"
OTPFile = "OTPGeneratedKey"
OTPCheatFIle = "../B/OTPGeneratedKey2"
LetterBinaryFile = "LetterBinary"
encryptedTextFile = "protocoloneoutput"


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


def generateFile(data, relativeFilePathAndName, convertToBinary=False):
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def generateOTPKeyFile():
    randomBits = random.getrandbits(OTPNumberOfBits)
    generateFile(randomBits, OTPFile, True)
    generateFile(randomBits, OTPCheatFIle, True)


def readFile(relativeFilePathAndName):
    try:
        with open(f"{relativeFilePathAndName}.dat", "r") as f:
            data = f.read()
            if data:
                return data
            else:
                raise Exception(f"No data in {relativeFilePathAndName}.dat file")
    except FileNotFoundError:
        print(f"File called {relativeFilePathAndName}.dat is not found")


def generateLetterToBinaryFile():
    text = readFile(LetterFile)
    data = textToBinary(text)
    generateFile(data, LetterBinaryFile)


def textToBinary(text):
    data = "".join(f"{ord(i):08b}" for i in text)
    return data


def binaryToText(binary):
    array = wrap(binary, 8)
    array = [int(i, 2) for i in array]
    text = "".join(map(chr, array))
    return text


def encryptAndDecryptOTP(plainOrCypherBinary, keyBinary):
    resultBinary = ""
    if len(plainOrCypherBinary) > len(keyBinary):
        raise Exception("plain/cypher Text is bigger than otp key.")
    for i, binary in enumerate(plainOrCypherBinary):
        resultBinary += str(int(binary) ^ int(keyBinary[i]))
    return resultBinary


def encryptLetter():
    generateLetterToBinaryFile()
    encryptedBinary = encryptAndDecryptOTP(
        readFile(LetterBinaryFile), readFile(OTPFile)
    )
    generateFile(encryptedBinary, encryptedTextFile)


if __name__ == "__main__":
    if not path.exists(OTPFile + ".dat"):
        generateOTPKeyFile()
    encryptLetter()
    sock = connectToServer()
    sendData(readFile(encryptedTextFile), sock)
    sock.close()
