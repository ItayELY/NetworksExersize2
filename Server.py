import socket
import os
import time
import utils

########################################################
client_dir = "/home/yonadav/NetworksExersize2/clients"
clients_dict = dict()
########################################################


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 12346))

    # open clients directory:
    # current_directory = os.getcwd()
    # final_directory = os.path.join(current_directory, r'clients')
    if not os.path.exists(client_dir):
        os.makedirs(client_dir)
    server.listen(5)

    while True:
        print("HI!")
        connected_socket, connected_address = server.accept()
        print('Connection from: ' + str(connected_address))
        while True:
            # receiving file details
            what_client_did = utils.receive_word(connected_socket)
            print("client wanted to" + what_client_did)
            if (what_client_did == "sending file"):
                print("receive file")
                file_size = utils.receive_word(connected_socket)
                file_path_from_root = utils.receive_word(connected_socket)
                print("Got a new file!" + file_path_from_root)
                utils.receive_file(os.path.join(client_dir, file_path_from_root), file_size, connected_socket)

            if (what_client_did == "sending directory"):
                dir_path = utils.receive_word(connected_socket)
                dir_absolute = os.path.join(client_dir, dir_path)
                utils.create_dir(os.path.join(client_dir, dir_path))

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
