import pandas as pd
S = pd.Series([100, 200, 300, 400], index=["A", "B", "C", "D"])
subset = S[["B", "D"]]
print("Subset (B and D):")
print(subset)