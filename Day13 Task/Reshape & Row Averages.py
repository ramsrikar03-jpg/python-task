import numpy as np
data = np.arange(1, 13)
matrix = data.reshape(3, 4)
print("Reshaped Matrix:\n", matrix)
row_averages = np.mean(matrix, axis=1)
print("\nRow Averages:", row_averages)