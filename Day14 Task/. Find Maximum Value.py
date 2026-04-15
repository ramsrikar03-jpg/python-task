import numpy as np
import pandas as pd
arr = np.array([12, 45, 22, 67, 34])
series = pd.Series(arr)
max_value = series.max()
print("Maximum Value:", max_value)