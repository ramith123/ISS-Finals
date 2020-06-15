# 816016584
"""This program encrypts and
sends letter to program B1 using OTP as the encryption method
"""

from socket import socket, gethostname
import random
from textwrap import wrap
from os import path

PORT = 1245  # Port used in program A1 and B1
OTPNumberOfBits = 1000  # OTP bits amount. If the message is longer than the otp key, It will not work. Change this number in that case

# File location and name. (Note: specifying ".dat" is not necessary)
LetterFile = "Letter"  # location of of the letter file.
OTPFile = "OTPGeneratedKey"  # Location to store the Random OTP key
OTPCheatFIle = "../B/OTPGeneratedKey2"  # This is the name of THE OTP key file that is transferred to Bob's computer through file explorer.This will only work if both A and B are in the same computer or share a network drive
LetterBinaryFile = "LetterBinary"  # Location of the Binary (ascii) converted Letter


encryptedTextFile = "protocoloneoutput"  # encrypted letter file


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


def sendData(message, sock):
    # Send server, specified by the socket object, a message. The message will be encoded before sending it.
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")

    except:
        print("Connection Error. Aborting")
        exit()


def generateFile(data, relativeFilePathAndName, convertToBinary=False):
    # create a ".dat" file containing <data> based on a location specified.

    # if true, it will convert the data (integer) into binary rep, and remove the first 2 characters ("0b" part)
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w") as f:
        f.write(data)


def generateOTPKeyFile():
    # Creates a random otp key in binary and create the file on local directory*.
    randomBits = random.getrandbits(OTPNumberOfBits)  # random bit generation
    generateFile(randomBits, OTPFile, True)  # Local copy of the key
    generateFile(
        randomBits, OTPCheatFIle, True
    )  # The file for Bob, if in same directory. (only used if B2 and A2 is not used)


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


def generateLetterToBinaryFile():
    # Function responsible for converting letter to binary data and storing it in a file
    text = readFile(LetterFile)
    data = textToBinary(text)
    generateFile(data, LetterBinaryFile)


def textToBinary(text):
    # Conversion of string text into a binary string. (Different from int to binary from generateFile())
    data = "".join(f"{ord(i):08b}" for i in text)
    return data


def binaryToText(binary):
    # Ascii binary to String character conversion
    array = wrap(binary, 8)  # Breaks String into chunks of 8 bits
    array = [
        int(i, 2) for i in array
    ]  # Convert array elements (String) to integer values but with base 2 (Binary)
    text = "".join(
        map(chr, array)
    )  # map each integer in the array chr(integer) and save it as a string
    return text


def encryptAndDecryptOTP(plainOrCypherBinary, keyBinary):
    # Function XOR the message with the OTP key. Since this is reversable, the same function can both decrypt and encrypt
    resultBinary = ""
    if len(plainOrCypherBinary) > len(keyBinary):  # If the the is smaller than the Text
        raise Exception("plain/cypher Text is bigger than otp key.")
    for i, binary in enumerate(
        plainOrCypherBinary
    ):  # xor each character then convert to String
        resultBinary += str(int(binary) ^ int(keyBinary[i]))
    return resultBinary


def encryptLetter():
    # Encrypts and stores Letter data
    generateLetterToBinaryFile()
    encryptedBinary = encryptAndDecryptOTP(
        readFile(LetterBinaryFile), readFile(OTPFile)
    )
    generateFile(encryptedBinary, encryptedTextFile)


if __name__ == "__main__":
    if not path.exists(OTPFile + ".dat"):  # If OTP file doesn't exist, generate one
        generateOTPKeyFile()
    encryptLetter()
    sock = connectToServer()  # Connect to server
    sendData(readFile(encryptedTextFile), sock)  # Send Data to server
    sock.close()  # connection close
