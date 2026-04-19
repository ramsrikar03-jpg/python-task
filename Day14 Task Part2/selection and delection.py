import pandas as pd
df = pd.DataFrame({
    "A": [10, 20, 30],
    "B": [5, 15, 25]
}, index=["x", "y", "z"])
row_y = df.loc["y"]
print("Selected Row 'y':\n", row_y)
df_updated = df.drop("x")
print("\nUpdated DataFrame (after deleting 'x'):\n", df_updated)