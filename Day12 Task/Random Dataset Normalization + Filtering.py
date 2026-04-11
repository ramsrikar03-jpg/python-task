import random
data = [random.random() for _ in range(8)]
print("Original Data:", data)
normalized = [x * 100 for x in data]
print("Normalized Data:", normalized)
filtered = [x for x in normalized if x > 50]
print("Filtered Data (>50):", filtered)
sorted_data = sorted(filtered)