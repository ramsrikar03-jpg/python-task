import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data
temps = np.array([28, 30, 32, 31, 29])

# Convert to Pandas Series
temp_series = pd.Series(temps)

print(temp_series)

# Plot line graph
plt.figure()
plt.plot(temp_series, marker='o')

# Add title and grid
plt.title("Daily Temperature Trend")
plt.xlabel("Day")
plt.ylabel("Temperature (°C)")
plt.grid()

plt.show()