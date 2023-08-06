import time

class FuncTimer:
    def measure(self, *args, **kwargs) -> None:
        def wrapper(func):
            __before = time.time()
            func()
            __after = time.time()
            __time = format((__after - __before), ".4f")
            print(f"🕜 {func.__name__} took: {__time} seconds!")
        return wrapper