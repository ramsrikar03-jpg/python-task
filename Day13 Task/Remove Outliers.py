import numpy as np
values = np.array([10, 12, 15, 18, 100, 14, 13])
mean = np.mean(values)
std_dev = np.std(values)
print("Mean:", mean)
print("Standard Deviation:", std_dev)
filtered_values = values[np.abs(values - mean) <= 2 * std_dev]
print("Filtered Values:", filtered_values)