import os
import time


def remove_prefix(str, prefix):
    if str.startswith(prefix):
        return str[len(prefix):]
    else:
        return str


def send_file(file_absolute_path, root, socket):
    file_size = os.path.getsize(file_absolute_path)

    file_path_from_root = remove_prefix(file_absolute_path, root)
    # if len(file_path_from_root) > 0:
    #     if file_path_from_root[0] == '/':
    #         file_path_from_root = file_path_from_root[1:]

    file_path_from_root = remove_sep_from_start_of_path(file_path_from_root)

    print("sending the following file: " + file_absolute_path)

    send_word("sending file", socket)
    send_word(file_size, socket)
    send_word(file_path_from_root, socket)
    # Opening file and sending data.
    with open(file_absolute_path, "rb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()
        # Running loop while c != file_size.
        while c < file_size:
            data = file.read(1024)
            if not (data):
                break
            socket.sendall(data)
            c += len(data)
        time.sleep(0.5)
        # Ending the time capture.
        end_time = time.time()
    print("File Transfer client Complete.Total time: ", end_time - start_time)


def send_word(word, socket):
    word = str(word) + '~'
    # Running loop while c != file_size.
    i = 0
    while True:
        socket.sendall(word[i].encode())
        if i + 1 == len(word):
            break
        i += 1


def send_dir(dir_absolute_path, root, socket):
    # send myself
    send_word("sending directory", socket)
    # send path from root
    relative = remove_prefix(dir_absolute_path, root)
    # if len(relative) > 0:
    #     if relative[0] == '/':
    #         relative = relative[1:]
    relative = remove_sep_from_start_of_path(relative)
    send_word(relative, socket)
    print("sending the following directory: " + dir_absolute_path)

    for filename in os.listdir(dir_absolute_path):
        full_path_of_filename = os.path.join(dir_absolute_path, filename)

        if os.path.isdir(full_path_of_filename):
            send_dir(full_path_of_filename, root, socket)
            continue

        if not os.path.isdir(full_path_of_filename):
            send_file(full_path_of_filename, root, socket)


def receive_file(file_name_absolute, file_size, socket):
    print("receiving the following file " + file_name_absolute)
    with open(file_name_absolute, "wb") as file:

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


def create_dir(dir_absolute_path):
    if not (os.path.exists(dir_absolute_path)):
        os.makedirs(dir_absolute_path)


def remove_sep_from_start_of_path(possibly_messed_up_path):
    if len(possibly_messed_up_path) > 0:
        if possibly_messed_up_path[0] == os.path.sep:
            possibly_messed_up_path = possibly_messed_up_path[1:]

    return possibly_messed_up_path


def stringify_event(watchdog_event, type):
    path = watchdog_event.src_path
    description = type + '$' + path
    return description


def get_path_of_stringified_event(event_description):
    splitted = event_description.split('$')
    path = splitted[1]
    return path


def get_type_of_stringified_event(event_description):
    splitted = event_description.split('$')
    type = splitted[0]
    return type


def notify_delete_file_or_dir(file_absolute_path, root, socket):
    # if (not os.path.exists(file_absolute_path)):
    #     return
    send_word("deleted file or directory", socket)
    file_path_from_root = remove_prefix(file_absolute_path, root)
    file_path_from_root = remove_sep_from_start_of_path(file_path_from_root)
    send_word(file_path_from_root, socket)


def delete_file_or_dir(absolute_path, socket):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # if file - delete it before recursive iteration
    if (os.path.exists(absolute_path)):
        if os.path.isfile(absolute_path):
            os.remove(absolute_path)
            time.sleep(0.5)
            return
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    for filename in os.listdir(absolute_path):
        full_path_of_filename = os.path.join(absolute_path, filename)

        delete_file_or_dir(full_path_of_filename, socket)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # if directory - delete it after recursive iteration
    if (os.path.exists(absolute_path)):
        if os.path.isdir(absolute_path):
            os.rmdir(absolute_path)
            time.sleep(0.5)
            return
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
