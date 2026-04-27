'''
=================================================================================================================================
 📊 Project Title: IGN Data Analysis
 Analyze IGN dataset using NumPy, Pandas, and Matplotlib
=================================================================================================================================
'''

'''
=================================================================================================================================
 📦 1. Import Required Libraries
=================================================================================================================================
 👉 Import numpy for numerical operations
 👉 Import pandas for data handling
 👉 Import matplotlib.pyplot for visualization
 👉 Import os for directory/file handling (optional)
=================================================================================================================================
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


'''
=================================================================================================================================
 🟢 SCENARIO 1: Data Loading & Preprocessing
=================================================================================================================================
 Tasks:
 1. Load dataset using Pandas
 2. Display:
    ○ First 5 rows
    ○ Last 5 rows
    ○ Dataset shape
 3. Remove unnecessary column ("Unnamed: 0")
 4. Check missing values in key columns
 5. Handle missing values:
    ○ Fill numeric columns with mean
    ○ Fill categorical columns with mode
 6. Ensure correct data types
=================================================================================================================================
'''

# Load dataset
data = pd.read_csv("C:/Users/Admin/Documents/pyCodes/data_Analytics/project_2/ign.csv")

# Display first 5 rows
print("First 5 rows:")
print(data.head())
print("------------------------------------------------------------------------------")

# Display last 5 rows
print("Last 5 rows:")
print(data.tail())
print("------------------------------------------------------------------------------")

# Display dataset shape
print("Dataset shape:")
print(data.shape)
print("------------------------------------------------------------------------------")

# Remove unnecessary column (if exists)
data.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
print("Removed 'Unnamed: 0' column (if present)")
print("------------------------------------------------------------------------------")

# Check missing values
missing_values = data[['score', 'genre', 'platform']].isnull().sum()
print("Missing values BEFORE handling:\n", missing_values)
print("------------------------------------------------------------------------------")

# Ensure score is numeric
data['score'] = pd.to_numeric(data['score'], errors='coerce')

# Fill missing numeric values with mean
avg_score = data['score'].mean()
data['score'].fillna(avg_score, inplace=True)

# Fill categorical values with mode
if not data['genre'].mode().empty:
    data['genre'].fillna(data['genre'].mode()[0], inplace=True)

if not data['platform'].mode().empty:
    data['platform'].fillna(data['platform'].mode()[0], inplace=True)

print("Missing values handled successfully")
print("------------------------------------------------------------------------------")

# Check missing values after cleaning
missing_values_after = data[['score', 'genre', 'platform']].isnull().sum()
print("Missing values AFTER handling:\n", missing_values_after)
print("------------------------------------------------------------------------------")

# Convert data types
data = data.astype({
    'score': 'float64',
    'release_year': 'int32',
    'release_month': 'int32',
    'release_day': 'int32'
})

print("Data types converted successfully")
print("------------------------------------------------------------------------------")


'''
=================================================================================================================================
 🟢 SCENARIO 2: Line Graph (Score Trend)
=================================================================================================================================
 Tasks:
 1. Group data by release_year
 2. Compute average score per year
 3. Convert to NumPy arrays
 4. Plot line graph
 5. Add title and labels
 6. Save graph
=================================================================================================================================
'''

# Group by year and calculate average score
grouped_year = data.groupby('release_year')['score'].mean()

print("Average score per year:")
print(grouped_year)
print("------------------------------------------------------------------------------")

# Convert to NumPy arrays
years = grouped_year.index.to_numpy()
avg_scores = grouped_year.values

# Plot line graph
plt.figure()
plt.plot(years, avg_scores, marker='o')
plt.title("Average Game Score Over Years")
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.tight_layout()
# plt.savefig("avg_score_trend.png")


'''
=================================================================================================================================
 🟡 SCENARIO 3: Filtering + Bar Chart
=================================================================================================================================
 Tasks:
 1. Filter games with score > 7
 2. Count games per platform
 3. Select top 10 platforms
 4. Convert to NumPy arrays
 5. Plot bar chart
=================================================================================================================================
'''

# Filter high-rated games
filtered_data = data[data['score'] > 7]

# Count per platform
top_rated_games = filtered_data.groupby('platform')['title'].count()

# Select top 10 platforms
top_10 = top_rated_games.sort_values(ascending=False).head(10)

# Convert to NumPy arrays
platforms = top_10.index.to_numpy()
counts = top_10.values

# Plot bar chart
plt.figure()
plt.bar(platforms, counts)
plt.title("Top 10 Platforms by High-Rated Games")
plt.xlabel("Platform")
plt.ylabel("Number of Games")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig("top_platforms_bar.png")


'''
=================================================================================================================================
 🟡 SCENARIO 4: Genre Distribution (Pie Chart)
=================================================================================================================================
 Tasks:
 1. Count games per genre
 2. Select top 5 genres
 3. Plot pie chart
=================================================================================================================================
'''

# Count games per genre
genre_counts = data['genre'].value_counts()

# Top 5 genres
top_5 = genre_counts.head(5)

# Prepare data
genres = top_5.index.to_numpy()
counts = top_5.values

# Plot pie chart
plt.figure()
plt.pie(counts, labels=genres, autopct='%1.1f%%')
plt.title("Genre Distribution")
plt.tight_layout()
# plt.savefig("genre_distribution.png")


'''
=================================================================================================================================
 🔴 SCENARIO 5: Advanced Analysis
=================================================================================================================================
 Part 1: Feature Engineering
 Part 2: NumPy Analysis
 Part 3: Visualization
 Part 4: Insights
=================================================================================================================================
'''

# Create score categories
data['score_category'] = np.where(
    data['score'] >= 9, "Excellent",
    np.where(data['score'] >= 7, "Good", "Average")
)

# Convert editors_choice to numeric
data['editors_choice'] = data['editors_choice'].map({'Y': 1, 'N': 0})


# Average score per year
yearly_avg = data.groupby('release_year')['score'].mean()

years = yearly_avg.index.to_numpy()
avg_scores = yearly_avg.values

# Calculate yearly growth
score_growth = np.diff(avg_scores)

print("Yearly score growth:")
print(score_growth)
print("------------------------------------------------------------------------------")


# Line plot
plt.figure()
plt.plot(years, avg_scores, marker='o')
plt.title("Average Score Trend Over Years")
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.tight_layout()


# Stacked bar chart
category_counts = data.pivot_table(
    index='release_year',
    columns='score_category',
    aggfunc='size',
    fill_value=0
)

category_counts.plot(kind='bar', stacked=True)
plt.title("Score Category Distribution per Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Games")
plt.xticks(rotation=45)
plt.tight_layout()


# Histogram
plt.figure()
plt.hist(data['score'], bins=20)
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.tight_layout()


# Insights
max_year = yearly_avg.idxmax()
max_score = yearly_avg.max()

print(f"Highest scoring year: {max_year} ({max_score:.2f})")

if score_growth.mean() > 0:
    print("Trend: Scores are increasing over time")
else:
    print("Trend: Scores are fluctuating or decreasing")

editors_avg = data.groupby('editors_choice')['score'].mean()

print("\nAverage score by editors_choice:")
print(editors_avg)

if editors_avg[1] > editors_avg[0]:
    print("Editors' Choice games tend to have higher scores")
else:
    print("No strong correlation with Editors' Choice")

'''
=================================================================================================================================
 END OF PROJECT
=================================================================================================================================
'''