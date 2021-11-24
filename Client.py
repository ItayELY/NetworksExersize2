import socket
import sys
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import string

serverIp = sys.argv[1]
serverPort = sys.argv[2]
folderPath = sys.argv[3]
#timeToUpdate = sys.argv[4]
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


if __name__ == "__main__":
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
    my_observer.schedule(my_event_handler, folderPath, recursive=go_recrsive)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


