from pathlib import Path
import threading
import time
from typing import Callable

# region Logging
import logging
from utils import get_logger

fname = Path(__file__).stem
logger = get_logger(__name__, fname, level=logging.DEBUG, file_level=logging.DEBUG)
# endregion

COUNTER = 0

N_WORKERS = 5
ITERATIONS = 10
WAIT_TIME = 0.1
LINE = "-" * 100
LOCK = threading.Lock()

should_take = WAIT_TIME * N_WORKERS * ITERATIONS


def add_one(val: int) -> int:
    time.sleep(WAIT_TIME)
    val += 1
    return val


def single_threaded_worker(task: Callable[[], None], wid: int = -1):
    global COUNTER
    for i in range(ITERATIONS):
        COUNTER = task(COUNTER)


def multi_threaded_worker_without_lock(task: Callable[[], None], wid: int = -1):
    global COUNTER
    for i in range(ITERATIONS):
        COUNTER = task(COUNTER)


def multi_threaded_worker_with_lock(task: Callable[[], None], wid: int = -1):
    global COUNTER
    for i in range(ITERATIONS):
        with LOCK:
            # logger.debug(f"-----------------Aquiring lock by {wid=}, {COUNTER=}-----------------")
            COUNTER = task(COUNTER)
            # logger.debug(f"-----------------Releasing lock by {wid=}, {COUNTER=}-----------------")


def main_non_threaded():
    for _ in range(N_WORKERS):
        single_threaded_worker(add_one)

    logger.info(f"Single-Threaded {COUNTER=}")


def main_threaded(use_lock: bool = False):
    worker = multi_threaded_worker_with_lock if use_lock else multi_threaded_worker_without_lock
    for wid in range(N_WORKERS):
        process = threading.Thread(target=worker, args=(add_one, wid))
        process.start()

    main_thread = threading.current_thread()
    for thread in threading.enumerate():
        if thread is main_thread:
            continue
        thread.join()

    title = "with lock" if use_lock else "without lock"
    logger.info(f"Multi-threaded {title} {COUNTER=}")


def run_mt(use_lock: bool = False):
    print(LINE)
    global COUNTER
    COUNTER = 0
    t = time.time()
    main_threaded(use_lock)
    title = "with lock" if use_lock else "without lock"
    logger.debug(f"Multi-threaded {title} took {time.time() - t:.2f} seconds, should have taken {should_take} seconds")
    print(LINE)


def run_st():
    print(LINE)
    global COUNTER
    COUNTER = 0
    t = time.time()
    main_non_threaded()
    logger.debug(f"Non-threaded took {time.time() - t:.2f} seconds, should have taken {should_take} seconds")
    print(LINE)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Run atomic counter using python")
    # create a boolean flag
    parser.add_argument("--multi", action=argparse.BooleanOptionalAction, help="Run multi-threaded")
    parser.add_argument("--lock", action=argparse.BooleanOptionalAction, help="Run multi-threaded with lock")
    args = parser.parse_args()
    if args.multi:
        if type(args.lock) == bool:
            run_mt(args.lock)
        else:
            run_mt(False)
            run_mt(True)
    elif args.multi is False:
        run_st()
    else:
        run_mt(False)
        run_mt(True)
        run_st()
