import numpy as np
import pandas as pd
marks = np.random.randint(0, 100, 5)
df = pd.DataFrame(marks, columns=["Marks"])
df["Status"] = "Fail"
df.loc[df["Marks"] >= 40, "Status"] = "Pass"
passed = df[df["Status"] == "Pass"]
mean = np.mean(df["Marks"])
print(df)
print("\nPassed Students:")
for i in range(len(passed)):
    print(passed.iloc[i]["Marks"])
print("\nAverage Marks:", mean)