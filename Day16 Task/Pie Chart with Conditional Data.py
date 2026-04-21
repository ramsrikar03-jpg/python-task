import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

scores = np.array([40, 60, 80, 30, 90])

s = pd.Series(scores)

pass_count = (s > 50).sum()
fail_count = (s <= 50).sum()

labels = ["Pass", "Fail"]
values = [pass_count, fail_count]

print("Pass:", pass_count)
print("Fail:", fail_count)

# Plot Pie Chart
plt.figure()
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title("Pass vs Fail Distribution")

plt.show()