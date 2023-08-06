from itertools import cycle
from threading import Thread
from time import sleep

class Loader:
    def __init__(self, desc="Loading...", timeout=0.1, end=''):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.end = end
        self.desc = desc
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\033[93m\r{self.desc} {c}\033[0m", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        print(f'\033[0;32m\r{self.end}\033[0m', flush=True)  # , end='')

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()
