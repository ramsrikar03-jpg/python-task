import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data
products = ["Pen", "Book", "Pencil"]
sales = np.array([50, 80, 40])

# Create DataFrame
df = pd.DataFrame({
    "Product": products,
    "Sales": sales
})

print(df)

# Plot Bar Chart
plt.figure()
plt.bar(df["Product"], df["Sales"])

# Add labels and title
plt.title("Product Sales")
plt.xlabel("Products")
plt.ylabel("Sales")

plt.show()