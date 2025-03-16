from socket import *


clientSocket = socket()
connectionPort = 1234


def get_page():
    clientSocket.connect(('localhost', connectionPort))
    http_request = "GET /HelloWorld.html HTTP/1.1\r\nHost: 0.0.0.0\r\nConnection: close\r\n\r\n"
    clientSocket.sendall(http_request.encode('utf-8'))


    response = b""
    while True:  # Fixed: Ensure all data is received
        data = clientSocket.recv(1024)
        if not data:
            break
        response += data

    print(response.decode('utf-8'))


def get_404_page():
    clientSocket.connect('localhost', connectionPort)
    http_request = "GET /Hello HTTP/1.1\r\nHost: 0.0.0.0\r\nConnection: close\r\n\r\n"
    clientSocket.sendall(http_request.encode('utf-8'))

    response = b""
    while True:  # Fixed: Ensure all data is received
        data = clientSocket.recv(1024)
        if not data:
            break
        response += data

    print(response.decode('utf-8'))



if __name__ == "__main__":
    get_page()
    get_404_page()