import numpy as np
import pandas as pd
arr = np.array([10, 25, 30, 15, 40])
series = pd.Series(arr)
filtered = series[series > 20]
