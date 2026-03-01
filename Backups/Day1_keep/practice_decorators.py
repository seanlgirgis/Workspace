# Python Decorators: Practice Workbench
# =====================================

print("--- Python Decorators Starter ---")
print("Run this file using: python D:\Workspace\practice_decorators.py\n")

# Your practice code will go here!
def say_hello():
    print("Hello from Citi!")
    
def run_twice(func):
    func()
    func()
    
run_twice(say_hello)