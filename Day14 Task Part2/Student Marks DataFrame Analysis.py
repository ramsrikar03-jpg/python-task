import pandas as pd
data = pd.DataFrame({
    "Name": ["A", "B", "C"],
    "Math": [80, 70, 60],
    "Science": [90, 60, 70]
})
data["Total"] = data["Math"] + data["Science"]
print("DataFrame with Total marks:")
print(data)
top_student = data.loc[data["Total"].idxmax()]
print("\nStudent with highest total marks:")
print(top_student)