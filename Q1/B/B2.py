from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from socket import socket, gethostname
from binascii import unhexlify


p = 7
g = 5
bSecretNumber = 593
PORT = 7892
OTPFile = "OTPGeneratedKey"
aesFile = "AESKeyFile"


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


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def generatePublicKey():
    return (g ** bSecretNumber) % p


def generateSharedKey(bSharableKey):
    key = (bSharableKey ** bSecretNumber) % p
    hashkey = sha256(str(key).encode())
    return hashkey.digest()


def sendPublicKey(connection):
    key = generatePublicKey()
    sendData(str(key), connection)


def getPublicKey(connection):
    key = receiveDataFromConnection(connection)
    return int(key)


def diffHelExchangeServer(connection):
    sendPublicKey(connection)
    bKey = getPublicKey(connection)
    return generateSharedKey(bKey)


def aesDecryption(key, message):
    cipher = AES.new(key, AES.MODE_ECB)
    result = cipher.decrypt(unhexlify(message))

    return unpad(result, AES.block_size).decode()


def generateOTPFile(key, encryptedOTP):
    message = aesDecryption(key, encryptedOTP)
    print("Message decryption complete.")
    generateFile(message, OTPFile)


if __name__ == "__main__":
    sock = makeServer()
    connection = listenForConnection(sock)

    key = diffHelExchangeServer(connection)
    print("Key exchange successful")
    generateFile(key.hex(), aesFile)

    encryptedOTP = receiveDataFromConnection(connection)
    print("Encryption message received.")
    generateOTPFile(key, encryptedOTP)
    print("Key decrypted and stored. server closed.")
    connection.close()
