import random
import socket
import os
import string
import time
import utils

########################################################
# Global Variables
dir_of_all_clients_path = "/home/yonadav/NetworksExersize2/clients"
root_dir_of_current_client = ""


########################################################

def accept_new_user(socket):
    global root_dir_of_current_client
    global dir_of_all_clients_path

    identifier = generate_identifier()
    os.makedirs(os.path.join(dir_of_all_clients_path, identifier))
    utils.send_word(identifier, socket)
    root_dir_of_current_client = os.path.join(dir_of_all_clients_path, identifier)



def handle_old_user(identifier, socket):
    user_dir_path = os.path.join(identifier, dir_of_all_clients_path)
    #send to client his dir
    utils.send_dir(user_dir_path,os.path.basename(user_dir_path), socket)



def welcome_client(socket):
    print("I am welcoming a new client!")
    connected_socket, connected_address = server.accept()
    print('Connection from: ' + str(connected_address))
    # Lets see if you are new to the club or not:
    identifier = utils.receive_word(connected_socket)
    if str(identifier) == "I am new to the club":
        accept_new_user(socket)
    else:
        handle_old_user(identifier ,socket)


def generate_identifier(chars=string.ascii_uppercase + string.ascii_lowercase + string.digits, N=128):
    return ''.join(random.choice(chars) for _ in range(N))


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 12345))

    # open clients directory:
    # current_directory = os.getcwd()
    # final_directory = os.path.join(current_directory, r'clients')
    if not os.path.exists(dir_of_all_clients_path):
        os.makedirs(dir_of_all_clients_path)
    server.listen(5)

    while True:
        print("I am up and running")
        connected_socket, connected_address = server.accept()
        print('Connection from: ' + str(connected_address))
        while True:
            # receiving file details
            what_client_did = utils.receive_word(connected_socket)
            print("client said he was " + what_client_did)
            if (what_client_did == "sending file"):
                print("receive file")
                file_size = utils.receive_word(connected_socket)
                file_path_from_root = utils.receive_word(connected_socket)
                print("Got a new file!" + file_path_from_root)
                utils.receive_file(os.path.join(root_dir_of_current_client, file_path_from_root), file_size,
                                   connected_socket)

            if (what_client_did == "sending directory"):
                dir_path = utils.receive_word(connected_socket)
                dir_absolute = os.path.join(root_dir_of_current_client, dir_path)
                utils.create_dir(os.path.join(root_dir_of_current_client, dir_path))

            if (what_client_did == "I want to register a new user"):
                accept_new_user(connected_socket)

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
