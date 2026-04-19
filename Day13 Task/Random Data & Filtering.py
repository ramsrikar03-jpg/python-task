import numpy as np
nums = np.random.randint(1, 100, 10)
print("Original Numbers:", nums)
filtered = nums[nums % 5 == 0]
sorted_result = np.sort(filtered)
print("Filtered & Sorted Values:", sorted_result)