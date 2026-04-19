import numpy as np
data = np.array([1, 2, 2, 3, 1, 4, 2, 3])
unique_values, counts = np.unique(data, return_counts=True)
print("Unique Values:", unique_values)
print("Counts:", counts)
result = dict(zip(unique_values, counts))
print("Number with Counts:", result)