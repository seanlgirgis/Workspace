def my_logger(func):
    def wrapper():
        print("--- Starting Execution ---"); func(); print("--- Finished Execution ---")
    return wrapper
@my_logger
def say_hello():
    print("Hello from Citi!")
say_hello()