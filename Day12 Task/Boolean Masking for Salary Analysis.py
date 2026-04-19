import numpy as np
salaries = np.array([25000, 40000, 15000, 50000, 30000])
mask = salaries > 30000
filtered = salaries[mask]
count = np.sum(mask)
print(filtered)  
print(count)    