from socket import socket, gethostname


port = 1245


def connectToServer():
    sock = socket()
    try:
        sock.connect((gethostname(), port))
        print("Server Connection successfull.")
        return sock
    except ConnectionRefusedError:
        print(f"Server Unavailable. make sure the port is {port}")
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


if __name__ == "__main__":

    sendData("Test", connectToServer())
