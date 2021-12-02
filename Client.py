import socket
import sys
import time
import os
import utils
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import string

root_dir = ''


def define_root_dir(full_path):
    global root_dir
    root_dir = full_path


serverIp = sys.argv[1]
serverPort = sys.argv[2]
folderPath = sys.argv[3]
timeToUpdate = sys.argv[4]
newFolder = True
if len(sys.argv) == 6:
    identifier = sys.argv[5]
    newFolder = False


def on_created(event):
    print(f"{event.src_path} has been created")


def on_deleted(event):
    print(f"{event.src_path} has been deleted")


def on_modified(event):
    print(f"{event.src_path} has been modified")


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


if __name__ == "__main__":
    # open socket:
    skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skClient.connect(('127.0.0.1', 12346))
    define_root_dir("/home/yonadav/Music/")
    utils.send_dir(os.path.join(root_dir, "filesOfClient"), root_dir, skClient)


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
