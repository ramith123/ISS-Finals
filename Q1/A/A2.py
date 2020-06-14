"""
This Program uses diffie heleman method to generate a symmetric key,
and use AES encryption to encrypt the OTP key from previous program
and send it to program B2
"""

from hashlib import sha256
from Crypto.Cipher import AES
from socket import socket, gethostname
from Crypto.Util.Padding import pad

p = 7
g = 5
aSecretNumber = 475  # Alice's secret Number used in Symmetric key generation
PORT = 7892  # Port used in program A1 and B1

# File location and name. (Note: specifying ".dat" is not necessary)
OTPFile = "OTPGeneratedKey"  # Location to store the Random OTP key
aesFile = "AESKeyFile"  # Location of the aes symmeteric key


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


def generateFile(data, relativeFilePathAndName="default", convertToBinary=False):
    # create a ".dat" file containing <data> based on a location specified.
    if (
        convertToBinary
    ):  # if true, it will convert the data (integer) into binary rep, and remove the first 2 characters ("0b" part)
        data = bin(data)[2:]
    with open(f"{relativeFilePathAndName}.dat", "w") as f:
        f.write(data)


def generatePublicKey():
    # Creates public value that will be sent to Bob openly.
    return (g ** aSecretNumber) % p


def generateSharedKey(bSharableKey):
    # Generate AES symmeteric Key using Bob's public value
    key = (bSharableKey ** aSecretNumber) % p
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


def diffHelExchangeClient(conn):
    # Use above three function to complete the diffie hellman key exchange
    bKey = getPublicKey(conn)
    sendPublicKey(conn)

    return generateSharedKey(bKey)


def aesEncryption(key, message):
    # Encrypt a message using The symmetric key
    cipher = AES.new(key, AES.MODE_ECB)
    # message must be padded to fit the AES block size. So a pad function is used
    result = cipher.encrypt(pad(message.encode(), AES.block_size))
    return result


def encryptOTPKey(key):
    # Reads OTPKey from file, encrypts and returns the hexadecimal value.
    otpKey = readFile(OTPFile)
    encryptedMsg = aesEncryption(key, otpKey)
    return encryptedMsg.hex()  # Hex value as a String


if __name__ == "__main__":
    # Diffie helman key exchange
    conn = connectToServer()
    key = diffHelExchangeClient(conn)
    print("Key exchange successful")

    # Save Symmetric key locally
    generateFile(key.hex(), aesFile)
    # Encrypt OTP key
    EncryptedMsg = encryptOTPKey(key)
    print("Encryption Complete.")
    # Send encrypted OTP key
    sendData(EncryptedMsg, conn)
    print("Encrypted message sent. Client closing.")
    conn.close()
