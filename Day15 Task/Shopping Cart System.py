cart = ["apple", "banana", "apple", "milk"]
cart = set(cart)
prices = {"apple": 50, "banana": 20, "milk": 30}
total = 0
for item in cart:
    try:
        total += prices[item]
    except:
        print(item, "not available")
print("Total cost:", total)