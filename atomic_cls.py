import threading
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

COUNTER = 0
N_WORKERS = 5
ITERATIONS = 10
WAIT_TIME = 0.01
should_take = WAIT_TIME * N_WORKERS * ITERATIONS


class Counter:
    def __init__(self, start=0, increment_by=1, using_multi_threading=False):
        self.lock = threading.Lock()
        self.start_value = start
        self.value = self.start_value
        self.increment_by = increment_by
        self.using_multi_threading = using_multi_threading

    def run(self, wid: str):
        try:
            if self.using_multi_threading:
                logger.debug(f"-----------------Aquiring lock by {wid=}{id(self.value)=}-----------------")
                self.lock.acquire()
            self.value += self.increment_by
        finally:
            if self.using_multi_threading:
                logger.debug(f"-----------------Releasing lock by {wid=}{id(self.value)=}-----------------")
                self.lock.release()
            pass


def worker(id: str, c: Counter):
    for i in range(ITERATIONS):
        time.sleep(WAIT_TIME)
        c.run(f"{id}:")
    logging.debug(f"worker:{id} done")


def main_multi_threaded():
    counter = Counter(using_multi_threading=True)
    for w_index in range(N_WORKERS):
        t = threading.Thread(
            target=worker,
            args=(
                str(w_index),
                counter,
            ),
        )
        t.start()

    logger.debug(f"Waiting for worker threads")
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    logging.info(f"Counter has value: {counter.value}")


def main_single_threaded():
    counter = Counter(using_multi_threading=False)
    for w_index in range(N_WORKERS):
        worker(str(w_index), counter)

    logging.info(f"Counter has value: {counter.value}")


def run_mt():
    t = time.time()
    main_multi_threaded()
    logger.debug(
        f"---------------Multi-threaded took {(time.time() - t):.2f} seconds, should have taken {should_take} seconds"
    )


def run_st():
    t = time.time()
    main_single_threaded()
    logger.debug(
        f"---------------Single-threaded took {(time.time() - t):.2f} seconds, should have taken {should_take} seconds"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Run atomic counter using python")
    # create a boolean flag
    parser.add_argument("--multi", action=argparse.BooleanOptionalAction, help="Run multi-threaded")
    args = parser.parse_args()
    if args.multi:
        run_mt()
    elif args.multi is False:
        run_st()
    else:
        run_mt()
        run_st()
