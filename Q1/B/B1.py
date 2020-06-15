# 816016584
"""
This program Receives and decrypts Alice's message and display it on the screen. 
"""
from socket import gethostname, socket
from textwrap import wrap
from os import path

PORT = 1245  # Port used in program A1 and B1

# Store location of encrypted letter sent by Alice
encryptedTextFile = "protocoloneoutput"

# Location of the decrypted Binary (ascii) converted Letter
decryptedTextFile = "LetterBinary"

OTPFile = "OTPGeneratedKey"  # Location to store the Random OTP key


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


def sendData(message, sock):
    # Send a server given message through given socket
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")

    except:
        print("Connection Error. Aborting")
        exit()


def getDataFromClient():
    # Function to make a server and get client data
    sock = makeServer()
    conn = listenForConnection(sock)
    data = receiveDataFromConnection(conn)
    conn.close()
    return data


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    # create a ".dat" file containing <data> based on a location specified.
    if (
        convertToBinary
    ):  # if true, it will convert the data (integer) into binary rep, and remove the first 2 characters ("0b" part)
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w") as f:
        f.write(data)


def decryptLetter():
    # Decrypt the Letter file using OTP key given by either B2, or stored locally. (logic handled in main)
    encryptedBinary = readFile(encryptedTextFile)
    decryptedBinary = encryptAndDecryptOTP(encryptedBinary, readFile(OTPFile))
    generateFile(decryptedBinary, decryptedTextFile)


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


if __name__ == "__main__":
    try:
        # get Encrypted Letter from Alice
        generateFile(getDataFromClient(), encryptedTextFile)

        # Logic to see the OTP exist or should wait for key, if it doesn't the local OTP key can be used (Note the local key is only available if alice is on the same machine or shares some common storage)
        if not path.exists(OTPFile + ".dat"):
            choice = input(  # If the OTP key has not been sent by A2 yet. This will pause the program until the user runs and gets OTP key from A2 and B2
                "OTP key file does not exist. Try running B2 then A2 and come back here. <ENTER> to continue.\n OR press <y> to use the local file (Only works if both programs on the same machine) :"
            )
            if choice == "y":  # Or the user can use the local OTP key
                OTPFile = "OTPGeneratedKey2"

        decryptLetter()

        print("\n")
        print(
            binaryToText(readFile(decryptedTextFile))
        )  # Convert decrypted binary to text and display on console
        print("\n")
    except:
        print("An error has occurred. Closing Program")
