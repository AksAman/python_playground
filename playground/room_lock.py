from pathlib import Path
import threading
import time
from typing import List

# region Logging
import logging
from utils import get_logger

fname = Path(__file__).stem
logger = get_logger(name=__name__, log_file_name=fname, level=logging.DEBUG, file_level=logging.DEBUG)
# endregion

WAIT_TIME = 0.6
LINE = "-" * 100
people_in_room: List[str] = []


def enter_open_room(person_name: str, lock: threading.Lock = None):
    global people_in_room
    logger.info(f"ENTER::{person_name} entered the room from thread {threading.current_thread().name}")
    if people_in_room:
        logger.warning(f"WARNING::{person_name} found the room occupied by {','.join(people_in_room)}")
    people_in_room.append(person_name)
    time.sleep(WAIT_TIME)
    logger.debug(f"WORK::{person_name} worked for {WAIT_TIME} seconds from thread {threading.current_thread().name}")
    logger.info(f"LEAVE::{person_name} left the room from thread {threading.current_thread().name}")
    people_in_room = []


def enter_locked_room(person_name: str, lock: threading.Lock):
    global people_in_room
    with lock:
        print("\n")
        logger.info(f"ENTER::{person_name} entered the room from thread {threading.current_thread().name}")
        if people_in_room:
            logger.warning(f"WARNING::{person_name} found the room occupied by {','.join(people_in_room)}")
        logger.debug(f"LOCKED::{person_name} locked the room from thread {threading.current_thread().name}")
        people_in_room.append(person_name)
        time.sleep(WAIT_TIME)
        logger.debug(
            f"WORK::{person_name} worked for {WAIT_TIME} seconds from thread {threading.current_thread().name}"
        )
        logger.debug(f"UNLOCKED::{person_name} unlocked the room from thread {threading.current_thread().name}")
        logger.info(f"LEAVE::{person_name} left the room from thread {threading.current_thread().name}\n")
        people_in_room = []


def run(use_lock: bool = False):
    print(LINE)
    global people_in_room
    people_in_room = []

    lock = threading.Lock() if use_lock else None
    room_entry_method = enter_locked_room if use_lock else enter_open_room
    title = "WITH LOCK" if use_lock else "WITHOUT LOCK"
    names: List[str] = ["Alice", "Bob", "Charlie", "David", "Eve"]
    for person_name in names:
        t = threading.Thread(target=room_entry_method, args=(person_name, lock)).start()

    for t in threading.enumerate():
        if t is not threading.current_thread():
            t.join()

    logger.debug(f"{title} Done\n")
    print(LINE)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Room lock example for multi-threading")
    parser.add_argument(
        "--lock",
        action=argparse.BooleanOptionalAction,
        help="Run multi-threaded with lock",
    )
    args = parser.parse_args()

    if args.lock:
        run(use_lock=True)
    elif args.lock is False:
        run(use_lock=False)
    else:
        run(use_lock=True)
        run(use_lock=False)
