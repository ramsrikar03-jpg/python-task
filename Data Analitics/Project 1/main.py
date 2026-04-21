#scenario 1
import pandas as pd
 
import numpy as np
 
import matplotlib.pyplot as plt
 
# Load data
 
df = pd.read_csv(r'C:\Users\Windows\Downloads\Python Practice\Analytics\Project 1\railway_gauges.csv')
print(df.head()) # Shows first 5 rows by default
print(df.columns)
# Check total missing values per column
 
print(df.isnull().sum())
 
# Replace all NaN values with 0
 
df.fillna(0, inplace=True)
 
gauge_cols = ['Broad Gauge', 'Metre Gauge', 'Narrow Gauge', 'Total']
 
df[gauge_cols] = df[gauge_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
 
#SCENARIO 2
year = df["Year"]
total = df["Total"]
# Plot
 
plt.figure(figsize=(12,6))
plt.plot(df['Year'], df['Total'])
plt.xticks(rotation=75)   # rotate so all years are visible
plt.xlabel("Year")
plt.ylabel("Total Tracks")
plt.title("Total Railway Tracks Over Years")
plt.show()
 
 
#scanario 3
df['Year_num'] = df['Year'].str[:4].astype(int)
 
# Convert year
df['Year_num'] = df['Year'].str[:4].astype(int)
 
# Filter
df2 = df[df['Year_num'] > 2000]
print(df2)
 
 
# Grouped bar chart
x = np.arange(len(df2))
w = 0.25
 
plt.bar(x, df2["Broad Gauge"], w, label="Broad")
plt.bar(x + w, df2["Metre Gauge"], w, label="Metre")
plt.bar(x + 2*w, df2["Narrow Gauge"], w, label="Narrow")
 
plt.xticks(x, df2["Year"], rotation=45)
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.title("Gauge Comparison After 2000")
plt.legend()
 
plt.show()
 
# Dominant gauge
dominant = df2[["Broad Gauge", "Metre Gauge", "Narrow Gauge"]].sum().idxmax()
print("Dominant Gauge:", dominant)
 
#Scenario 4
# 1. Calculate total sum
totals = df[["Broad Gauge", "Metre Gauge", "Narrow Gauge"]].sum()
 
# 2. Create new structure (Series)
print("Total Values:\n", totals)
 
# 3. Plot pie chart
plt.pie(totals, labels=totals.index, autopct="%1.1f%%")
 
# 4. Title
plt.title("Contribution of Railway Gauges")
 
plt.show()
 
# 5. Interpretation
print("Highest Contribution:", totals.idxmax())
 
#scanario 5
# Convert Year for analysis
df["Year_num"] = df["Year"].astype(str).str[:4].astype(int)
 
# --------------------------------------------------
# 1. Percentage Columns
df["% Broad"] = (df["Broad Gauge"] / df["Total"]) * 100
df["% Metre"] = (df["Metre Gauge"] / df["Total"]) * 100
df["% Narrow"] = (df["Narrow Gauge"] / df["Total"]) * 100
 
# --------------------------------------------------
# 2. Yearly Growth using NumPy
growth = np.diff(df["Total"])
 
# --------------------------------------------------
# 3. Line Graph (All Gauges)
plt.figure()
plt.plot(df["Year"], df["Broad Gauge"], label="Broad")
plt.plot(df["Year"], df["Metre Gauge"], label="Metre")
plt.plot(df["Year"], df["Narrow Gauge"], label="Narrow")
 
plt.title("Railway Gauges Trend")
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.xticks(rotation=90)
plt.legend()
plt.show()
 
# --------------------------------------------------
# 3. Stacked Bar Chart
plt.figure()
plt.bar(df["Year"], df["Broad Gauge"], label="Broad")
plt.bar(df["Year"], df["Metre Gauge"], bottom=df["Broad Gauge"], label="Metre")
plt.bar(df["Year"], df["Narrow Gauge"],
        bottom=df["Broad Gauge"] + df["Metre Gauge"], label="Narrow")
 
plt.title("Gauge Composition")
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.xticks(rotation=90)
plt.legend()
plt.show()
 
# --------------------------------------------------
# 4. Highlights
 
# Highest growth year
max_growth_year = df["Year"].iloc[np.argmax(growth) + 1]
print("Highest Growth Year:", max_growth_year)
 
# Check decline
if any(growth < 0):
    print("Decline observed in some years")
else:
    print("No decline observed")