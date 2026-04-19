import math
students = [("A", 45), ("B", 67), ("C", 80), ("D", 30)]
student_dict = dict(students)
passed_students = {}
total = 0
count = 0
for name, marks in student_dict.items():
    if marks > 50:
        passed_students[name] = marks
        total += marks
        count += 1
average = math.floor(total / count) if count > 0 else 0
with open("result.txt", "w") as file:
    file.write("Passed Students:\n")
    for name, marks in passed_students.items():
        file.write(f"{name}: {marks}\n")
    file.write(f"\nAverage Marks: {average}")
print("Process completed! Check result.txt file.")