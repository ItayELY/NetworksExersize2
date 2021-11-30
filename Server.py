import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12345))

if __name__ == "__main__":
    #open clients directory:
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'clients')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)
        file_name = client_socket.recv(1024)
        print('Received: ', file_name)
        #creating new client directory:
        client_directory = os.path.join(final_directory + file_name, r'client1')
        sData = client_socket.recv(1024)
        while sData:
            fDownloadFile = open(client_directory, "wb")
            #endfile- special packet indicates file ended.
            while sData != "endfile":
                fDownloadFile.write(sData)
                sData = client_socket.recv(1024)
        print("Download Completed")
        break
