# 1. List comprehension (creates the full list in memory)
big_list = [x**2 for x in range(1, 500001)]

# 2. Generator expression (lazy, almost no memory used for the structure itself)
big_gen = (x**2 for x in range(1, 500001))

# 3. Compare their memory usage
import sys

print(f"big_list   size: {sys.getsizeof(big_list):,} bytes")
print(f"big_gen    size: {sys.getsizeof(big_gen):,} bytes")