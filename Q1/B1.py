from socket import gethostname, socket
from textwrap import wrap

PORT = 1245

encryptedTextFile = "protocoloneoutput2"
decryptedTextFile = "LetterBinary2"
OTPFile = "OTPGeneratedKey2"


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


def encryptAndDecryptOTP(plainOrCypherBinary, keyBinary):
    resultBinary = ""
    if len(plainOrCypherBinary) > len(keyBinary):
        raise Exception("plain/cypher Text is bigger than otp key.")
    for i, binary in enumerate(plainOrCypherBinary):
        resultBinary += str(int(binary) ^ int(keyBinary[i]))
    return resultBinary


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
            if len(data) < 1024:
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


def getDataFromClient():
    sock = makeServer()
    conn = listenForConnection(sock)
    data = receiveDataFromConnection(conn)
    conn.close()
    return data


def generateFile(data, relativeFilePathAndName, convertToBinary=False):
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def decryptLetter():
    encryptedBinary = readFile(encryptedTextFile)
    decryptedBinary = encryptAndDecryptOTP(encryptedBinary, readFile(OTPFile))
    generateFile(decryptedBinary, decryptedTextFile)


def binaryToText(binary):
    array = wrap(binary, 8)  # break array into chunks of 8 bits.
    array = [int(i, 2) for i in array]
    text = "".join(map(chr, array))
    return text


if __name__ == "__main__":
    try:
        generateFile(getDataFromClient(), encryptedTextFile)
        decryptLetter()
        print("\n")
        print(binaryToText(readFile(decryptedTextFile)))
        print("\n")
    except:
        print("An error has occured. Closing Program")
