import copy
employees = [[101, "A"], [102, "B"], [103, "C"]]
shallow_employees = employees[:] 
shallow_employees[0][1] = "Z"
print("Original:", employees) 
print("Shallow:", shallow_employees)