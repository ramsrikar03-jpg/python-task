import pandas as pd
cities = {"Delhi": 2000000, "Mumbai": 3000000, "Chennai": 1500000}
city_index = ["Delhi", "Chennai", "Bangalore"]
series = pd.Series(cities, index=city_index)
print("City Population Series:")
print(series)
missing = series[series.isna()]
print("\nCities with missing values:")
print(missing)