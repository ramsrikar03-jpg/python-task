import numpy as np
import pandas as pd
arr = np.array([10, np.nan, 30, np.nan, 50])
series = pd.Series(arr)
mean_value = series.mean()
updated_series = series.fillna(mean_value)
print("Original Series:")
print(series)
print("\nMean value:", mean_value)
print("\nUpdated Series:")
print(updated_series)