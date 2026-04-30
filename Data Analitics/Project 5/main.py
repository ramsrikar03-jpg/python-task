# ==========================================================================================================
# 📊 SCENARIO 5: Present Price vs Selling Price (Scatter Plot)
# Check whether cars with higher present price also have higher selling price.
# ==========================================================================================================
# 👉 Tasks:
# ● Select:
#   ○ Present_Price
#   ○ Selling_Price
# ● Remove missing values if any.
# ● Take a smaller sample (for example first 50 or 100 rows) using Pandas.
# ● Convert both columns into NumPy arrays.
# ● Plot a scatter plot using Matplotlib:
#   ○ X-axis → Present_Price
#   ○ Y-axis → Selling_Price
# ● Add:
#   ○ title
#   ○ x-label
#   ○ y-label
# ● Observe whether there is a positive relationship.
# ● Save the graph.
# ==========================================================================================================

# Select required columns
price_data = df[["Present_Price", "Selling_Price"]]

# Remove missing values
price_data = price_data.dropna()

# Take a smaller sample (first 100 rows)
price_sample = price_data.head(100)

# Convert to NumPy arrays
present_price = price_sample["Present_Price"].to_numpy()
selling_price = price_sample["Selling_Price"].to_numpy()

# Plot scatter plot
plt.figure()
plt.scatter(present_price, selling_price)

# Add labels and title
plt.title("Present Price vs Selling Price")
plt.xlabel("Present Price")
plt.ylabel("Selling Price")

# Save the graph
plt.savefig("present_vs_selling_price.png")

# Show plot
plt.show()


# ==========================================================================================================
# 📊 SCENARIO 6: Car Age Category Analysis + Bar Chart
# Create a new feature using year and compare car categories.
# ==========================================================================================================
# 👉 Tasks:
# ● Create a new column using Pandas:
#   Car Age Category
# ● Year >= 2015 → "New"
# ● 2010 to 2014 → "Medium"
# ● < 2010 → "Old"
# ● Count number of cars in each:
#   ○ Car Age Category
# ● Convert category names and counts into NumPy arrays.
# ● Plot a bar chart using Matplotlib:
#   ○ X-axis → Car Age Category
#   ○ Y-axis → Count
# ● Add title and labels.
# ● Save the graph.
# ==========================================================================================================

# Create Car Age Category column
def categorize_car(year):
    if year >= 2015:
        return "New"
    elif 2010 <= year <= 2014:
        return "Medium"
    else:
        return "Old"

df["Car_Age_Category"] = df["Year"].apply(categorize_car)

# Count number of cars in each category
category_counts = df["Car_Age_Category"].value_counts()

# Convert to NumPy arrays
categories = category_counts.index.to_numpy()
counts = category_counts.values

# Plot bar chart
plt.figure()
plt.bar(categories, counts)

# Add title and labels
plt.title("Car Age Category Distribution")
plt.xlabel("Car Age Category")
plt.ylabel("Number of Cars")

# Save the graph
plt.savefig("car_age_category_bar_chart.png")

# Show plot
plt.show()