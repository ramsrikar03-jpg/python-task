import pandas as pd
df = pd.DataFrame({
    "Name": ["A", "B", "C", "D"],
    "Marks": [50, 80, 30, 90]
})
df["Status"] = df["Marks"].apply(lambda x: "Pass" if x >= 50 else "Fail")
print("DataFrame with Status:\n", df)
passed_students = df[df["Status"] == "Pass"]
print("\nPassed Students:\n", passed_students)
average_marks = passed_students["Marks"].mean()
print("\nAverage Marks of Passed Students:", average_marks)



