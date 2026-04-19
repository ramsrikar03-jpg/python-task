import numpy as np
ratings = np.array([2, 3, 4, 5, 1])
min_val = np.min(ratings) 
max_val = np.max(ratings)
normalized = (ratings - min_val) / (max_val - min_val)
print(normalized)
