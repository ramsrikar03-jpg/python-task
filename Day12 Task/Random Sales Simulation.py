import numpy as np
sales_data = np.random.randint(100, 501, size=10)
print("10 Days Sales Simulation:", sales_data)
average_sale = np.mean(sales_data)
print(f"Average Sale: {average_sale:.2f}")