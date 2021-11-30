import socket
import os
import time



def receive_file(file_name, file_size, directory, socket):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, directory, file_name)
    print(final_directory)
    with open(final_directory, "wb") as file:
        print("file size is " + str(file_size))
        print("file names is " + file_name)
        c = 0
        # Starting the time capture.
        start_time = time.time()

        # Running the loop while file is received.
        while c < int(file_size):
            data = socket.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)

        # Ending the time capture.
        end_time = time.time()

    print("File transfer Complete.Total time: ", end_time - start_time)

def receive_word(socket):
    put_word_in_me = ''
    c = 0
    while True:
        data = socket.recv(1).decode()
        if data == '~':
            break
        put_word_in_me = put_word_in_me + data
        c += len(data)
    return put_word_in_me
if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 12345))

    #open clients directory:
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'clients')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    server.listen(5)

    while True:
        print("HI!")
        connected_socket, connected_address = server.accept()
        print('Connection from: ' + str(connected_address))
        #receiving file details

        #file_name = connected_socket.recv(5).decode()
        #file_size = connected_socket.recv(3).decode()
        file_name = receive_word(connected_socket)
        file_size = receive_word(connected_socket)
        print("file size is " + file_size)
        print("file names is " + file_name)

        #writing received file to directory
        receive_file(file_name, file_size, "clients", connected_socket)


        # client_socket, client_address = server.accept()
        # print('Connection from: ', client_address)
        # file_name = client_socket.recv(1024)
        # print('Received: ', file_name)
        # #creating new client directory:
        # client_directory = os.path.join(final_directory + file_name, r'client1')
        # sData = client_socket.recv(1024)
        # while sData:
        #     fDownloadFile = open(client_directory, "wb")
        #     #endfile- special packet indicates file ended.
        #     while sData != "endfile":
        #         fDownloadFile.write(sData)
        #         sData = client_socket.recv(1024)
        # print("Download Completed")
        # break
