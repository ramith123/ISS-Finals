# 816016584
"""
This program sets up a symmetric key between Alice and Bob;
and decrypts the OTP key sent by alex using AES algorithm + symmetric key.
"""

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from socket import socket, gethostname
from binascii import unhexlify


p = 7  # prime number used from instructions
g = 5  # Generator number used from instructions
bSecretNumber = 593  # Bob's secret key to generate symmetric key
PORT = 7892  # Port used in program A1 and B1
OTPFile = "OTPGeneratedKey"  # Location to store the OTP key
aesFile = "AESKeyFile"  # Location of the aes symmeteric key


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
    # Send server, specified by the socket object, a message. The message will be encoded before sending it.
    try:
        print("trying to send message...")
        sock.sendall(message.encode())
        print("Message sent, Closing Connection.")

    except:
        print("Connection Error. Aborting")
        exit()


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    # create a ".dat" file containing <data> based on a location specified.

    # if true, it will convert the data (integer) into binary rep, and remove the first 2 characters ("0b" part)
    if convertToBinary:
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w+") as f:
        f.write(data)


def generatePublicKey():
    # Creates public value that will be sent to Bob openly.
    return (g ** bSecretNumber) % p


def generateSharedKey(bSharableKey):
    # Generate AES symmeteric Key using Bob's public value
    key = (bSharableKey ** bSecretNumber) % p
    hashkey = sha256(str(key).encode())
    return hashkey.digest()


def sendPublicKey(connection):
    # Send public key to a connection socket object
    key = generatePublicKey()
    sendData(str(key), connection)


def getPublicKey(connection):
    # Get Key from Connection Socket object return it.
    key = receiveDataFromConnection(connection)
    return int(key)


def diffHelExchangeServer(connection):
    # Use above three function to complete the diffie hellman key exchange
    sendPublicKey(connection)
    bKey = getPublicKey(connection)
    return generateSharedKey(bKey)


def aesDecryption(key, message):
    # Decrypt message using The symmetric key and returns the string with padding removed
    cipher = AES.new(key, AES.MODE_ECB)
    result = cipher.decrypt(unhexlify(message))

    return unpad(result, AES.block_size).decode()


def generateOTPFile(key, encryptedOTP):
    # Decrypt and save OTP Key
    message = aesDecryption(key, encryptedOTP)
    print("Message decryption complete.")
    generateFile(message, OTPFile)


if __name__ == "__main__":
    # create server and establish connection
    sock = makeServer()
    connection = listenForConnection(sock)

    # Generate and save Symmetric key
    key = diffHelExchangeServer(connection)
    print("Key exchange successful")
    generateFile(key.hex(), aesFile)

    # Decrypt and save OTP key
    encryptedOTP = receiveDataFromConnection(connection)
    print("Encryption message received.")
    generateOTPFile(key, encryptedOTP)
    print("Key decrypted and stored. server closed.")
    connection.close()
