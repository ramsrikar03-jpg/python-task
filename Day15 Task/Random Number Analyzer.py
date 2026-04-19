import random
numbers = []
for i in range(10):
    num = random.randint(1, 100)
    numbers.append(num)
print("Generated Numbers:", numbers)
even_count = 0
odd_count = 0
for num in numbers:
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1
print("Even count:", even_count)
print("Odd count:", odd_count)
unique_numbers = list(set(numbers))
print("Unique Numbers:", unique_numbers)