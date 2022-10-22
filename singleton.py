import time
from typing import Any
import logging

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any):
        if cls not in cls._instances:
            logger.debug(f"{cls=} {type(cls)=}")
            instance = super.__call__(*args, **kwds)
            logger.debug(f"Created {instance=}, {type(instance)=}")
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def execute(self):
        print("Executing")
        time.sleep(1)
        print("Execution complete")


def run():
    s1 = Singleton()
    s2 = Singleton()
    if id(s1) == id(s2):
        logger.info(
            f"Singleton successful, both objects have the same id: {id(s1)=}=={id(s2)=}"
        )
    else:
        logger.error(
            f"Singleton failed, both objects have different id: {id(s1)=}!={id(s2)=}"
        )


if __name__ == "__main__":
    run()
