class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
employees = {}
for i in range(2):
    name = input("Name: ")
    try:
        salary = int(input("Salary: "))
        employees[name] = Employee(name, salary)
    except:
        print("Invalid salary")
with open("emp.txt", "w") as f:
    for e in employees.values():
        f.write(e.name + " " + str(e.salary) + "\n")
for e in employees.values():
    print(e.name, e.salary)