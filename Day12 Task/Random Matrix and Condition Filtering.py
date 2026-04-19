import numpy as np
matrix = np.random.randint(0, 51, size=(3, 3))
print("Original Matrix:\n", matrix)
filtered_elements = matrix[matrix > 25]
print("\nElements greater than 25:")
print(filtered_elements)
