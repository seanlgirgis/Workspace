# Python Generators: Practice Workbench
# ====================================




def bad_function(num: int):
    result = []
    for i in range(num):
        result.append(i)
    return result

def good_generator(num: int):
    for i in range(num):
        yield i
        
       
import sys
# 1. Store the results in memory
bad_crash = bad_function(1000000) # 1 Million numbers
good_safe = good_generator(1000000)
# 2. Weigh them!
print(f"Bad Function size in RAM: {sys.getsizeof(bad_crash):,} bytes")
print(f"Good Generator size in RAM: {sys.getsizeof(good_safe):,} bytes")
    

