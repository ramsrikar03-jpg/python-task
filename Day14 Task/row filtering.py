import numpy as np
import pandas as pd
arr = np.array([
    [100, 200],
    [150, 250],
    [80, 120],
    [300, 400]])
df = pd.DataFrame(arr, columns=["Sales", "Profit"])
print("Original DataFrame:")
print(df)
filtered_df = df[df["Sales"] > 100]
print("\nFiltered DataFrame (Sales > 100):")
print(filtered_df)
avg_profit = filtered_df["Profit"].mean()
print("\nAverage Profit of filtered rows:", avg_profit)