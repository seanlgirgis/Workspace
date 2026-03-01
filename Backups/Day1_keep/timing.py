import time

def timer(func):
    def wrapper():
        start = time.time()
        func()                           # Call the original function
        end = time.time()
        print(f"Execution took: {end - start:.4f} seconds")
    return wrapper

@timer
def heavy_computation():
    print("Starting heavy work...")
    time.sleep(2)
    print("Heavy computation complete!")

# Run it!
heavy_computation()