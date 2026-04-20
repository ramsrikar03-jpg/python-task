import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
salaries = np.array([25000, 30000, 28000, 40000, 50000, 35000])
departments = ["HR", "IT", "HR", "IT", "Sales", "Sales"]
df = pd.DataFrame({
    "Salary": salaries,
    "Department": departments
})

print(df)

plt.figure()
plt.plot(df.index, df["Salary"], marker='o')
plt.title("Salary Trend")
plt.xlabel("Index")
plt.ylabel("Salary")
plt.show()

dept_salary = df.groupby("Department")["Salary"].mean()

plt.figure()
dept_salary.plot(kind='bar')
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.show()

dept_count = df["Department"].value_counts()

plt.figure()
dept_count.plot(kind='pie', autopct='%1.1f%%')
plt.title("Department Distribution")
plt.ylabel("")
plt.show()

plt.figure()
plt.hist(df["Salary"], bins=5)
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.show()

plt.figure()
plt.scatter(df.index, df["Salary"])
plt.title("Index vs Salary")
plt.xlabel("Index")
plt.ylabel("Salary")
plt.show()