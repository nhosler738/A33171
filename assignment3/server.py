import socket
import os
import threading

hostname = ''
serverPort = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows for reusing the port
print("Server socket created successfully")

serverSocket.bind((hostname, serverPort))
serverSocket.listen(5)
print("server socket is listening on port", serverPort)

# get file name from clients http request 
# ensures that all headers are received to support browser requests
def parse_http_request(client_socket):

    try:
        client_request = ""

        # loop through all request headers to ensure all are read
        while True:
            chunk = client_socket.recv(1024).decode('utf-8')
            client_request += chunk

            if '\r\n\r\n' in client_request:
                break
        
        print("Client request:\n", client_request)

        first_line = client_request.split('\r\n')[0]
        parts = first_line.split(' ')

        # check if the request is valid and contains the file name
        if len(parts) >= 2 and parts[0] == 'GET':
            filename = parts[1].lstrip('/')
            print(f"Extracted filename: {filename}")

            # check for 'User-Agent to detect if the request is from a browser
            headers = client_request.split('\r\n')
            user_agent = None
            for header in headers:
                if header.startswith('User-Agent:'):
                    user_agent = header[len('User-Agent:'):]
                    break
            
            if user_agent:
                print(f"Detected browser request: {user_agent}")
            
            return filename
        
        return None
    except Exception as e:
        print(f"Error parsing request: {e}")
        return None
    

        
# searched for filename and returns to client 
def return_file(filename, client_socket):


    try:
        html_path = os.path.join("templates", filename) 
        # if filepath exists: return file
        if(os.path.exists(html_path)):
            with open(html_path, "r") as file:
                response_body = file.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Type: {len(response_body)}\r\n"
                    "Connection: keep-alive\r\n\r\n"
                    f"{response_body}"
                )
        # if filepath doesn't exist: return 404 file
        else:
            with open("templates/404.html", "r") as file:
                response_body = file.read()
                response = (
                    "HTTP/1.1 404 NOT FOUND\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "Connection: keep-alive\r\n\r\n"
                    f"{response_body}"
                )

        # send response to client 
        client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error serving file: {e}")  


# handles individual client connections
def handle_client(client_socket):
    while True:
        file_requested = parse_http_request(client_socket=client_socket)
        if not file_requested:
            break # exit (client disconnected)
        return_file(filename=file_requested, client_socket=client_socket)

    print("Client disconnected")
    client_socket.close()





# main server loop listening for client connections
while True:
    # establish connection with client
    client_socket, client_address = serverSocket.accept()
    print("Connection:", client_address)

    # handle each client in a new thread for better scalability
    threading.Thread(target=handle_client, args=(client_socket,)).start()


    
    
    









      


