prices = [100, 200, 300, 400]
discounted_prices = [price * 0.9 if price > 200 else price for price in prices]
print(discounted_prices)
