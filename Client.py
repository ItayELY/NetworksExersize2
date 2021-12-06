import socket
import sys
import time
import os
import utils
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import string

########################################################
# Global Variables
root_dir = ''
serverIp = sys.argv[1]
serverPort = sys.argv[2]
argDirPath = sys.argv[3]
timeToUpdate = sys.argv[4]
changes_to_be_pushed = set()
debugPort = 12342

new_to_the_club = True
if len(sys.argv) == 6:
    identifier = sys.argv[5]
    new_to_the_club = False


########################################################


def define_root_dir(full_path):
    global root_dir
    root_dir = full_path


def on_created(event):
    print(f"{event.src_path} has been created")
    description = utils.stringify_event(event, "modified_or_created")
    changes_to_be_pushed.add(description)


def on_deleted(event):
    print(f"{event.src_path} has been deleted")
    description = utils.stringify_event(event, "deleted")
    changes_to_be_pushed.add(description)


def on_modified(event):
    print(f"{event.src_path} has been modified")
    description = utils.stringify_event(event, "modified_or_created")
    if utils.get_file_or_dir_of_stringified_event(description) == "file":
        changes_to_be_pushed.add(description)


def on_moved(event):
    print(f"{event.src_path} has been moved to {event.dest_path}")


#####


# for filename in os.listdir(final_dir):
#     if os.path.isdir(filename):
#         # print(os.path.join(directory, filename))
#         send_dir(os.path.join(dir_name,filename),socket)
#         continue
#     else:
#         send_file(os.path.join(dir_name,filename),socket)


def subscribe_new_user(root_dir, socket):
    utils.send_word("I want to register a new user", socket)
    utils.send_word("I am new to the club", socket)
    global identifier
    identifier = utils.receive_word(socket)
    print("Just received identifier from server: " + identifier)
    print("Proceeding to send root directory to server")
    utils.send_dir(root_dir, root_dir, socket)


def sign_up_existing_user(root_path, socket):
    utils.create_dir(root_path)
    utils.send_word("send me directory by identifier, please", socket)
    utils.send_word(identifier, socket)
    # main loop
    while True:
        what_server_said = utils.receive_word(socket)
        if (what_server_said == "sending file"):
            print("receive file")
            file_size = utils.receive_word(socket)
            file_path_from_root = utils.receive_word(socket)
            print("Got a new file!" + file_path_from_root)
            utils.receive_file(os.path.join(root_path, file_path_from_root), file_size,
                               socket)

        if (what_server_said == "sending directory"):
            dir_path = utils.receive_word(socket)
            dir_absolute = os.path.join(root_path, dir_path)
            utils.create_dir(os.path.join(root_path, dir_path))

        if (what_server_said == "finished sending root directory"):
            utils.send_word("finished for now", skClient)
            return


def run_watchdog():
    # Watchdog
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    go_recrsive = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, root_dir, recursive=go_recrsive)

    my_observer.start()
    try:
        while True:
            time.sleep(int(timeToUpdate))
            handel_changes()
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def handel_changes():
    changes_set = changes_to_be_pushed.copy()
    for change in changes_set:
        type = utils.get_type_of_stringified_event(change)
        absolute_path = utils.get_path_of_stringified_event(change)
        skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skClient.connect(('127.0.0.1', debugPort))
        utils.send_word(identifier, skClient)
        if type == "deleted":
            utils.notify_delete_file_or_dir(absolute_path, root_dir,
                                            skClient)

        if type == "modified_or_created":
            if os.path.isdir(absolute_path):
                utils.send_dir(absolute_path, root_dir, skClient)
            if os.path.isfile(absolute_path):
                utils.send_file(absolute_path, root_dir, skClient)
        utils.send_word("finished for now", skClient)
    changes_to_be_pushed.clear()


if __name__ == "__main__":
    # open socket:
    skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skClient.connect(('127.0.0.1', debugPort))

    define_root_dir("/home/yonadav/Music/")

    if new_to_the_club:
        utils.send_word("I am new here, don't have identifier yet...", skClient)
        subscribe_new_user(root_dir, skClient)

    if not new_to_the_club:
        utils.send_word(identifier, skClient)
        sign_up_existing_user(root_dir, skClient)
        utils.create_dir(argDirPath)
    print("returned to main of client")
    run_watchdog()

    # utils.send_dir(os.path.join(root_dir, "filesOfClient"), root_dir, skClient)

    # send_file("a.txt",skClient)

    #
    # #going through each file in given folder
    # for file_name in os.listdir(folderPath):
    #     #opening the file and sending to the server 1024b at a time:
    #     file = open(file_name, "wb")
    #     skClient.send(file)
    #     sRead = file.read(1024)
    #     while sRead:
    #         skClient.send(sRead)
    #         sRead = file.read(1024)
    #     skClient.send("endfile")
    #
    #
    # #Watchdog
    # patterns = ["*"]
    # ignore_patterns = None
    # ignore_directories = False
    # case_sensitive = True
    # my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    #
    # my_event_handler.on_created = on_created
    # my_event_handler.on_deleted = on_deleted
    # my_event_handler.on_modified = on_modified
    # my_event_handler.on_moved = on_moved
    #
    # go_recrsive = True
    # my_observer = Observer()
    # my_observer.schedule(my_event_handler, folderPath, recursive=go_recrsive)
    #
    # my_observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     my_observer.stop()
    #     my_observer.join()
