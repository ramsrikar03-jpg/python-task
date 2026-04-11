import copy
classes = [["Math", [30, 35]], ["Science", [25, 28]]]
classes_deep_copy = copy.deepcopy(classes)
classes[0][1][0] = 999 
print("Original Classes:   ", classes)
print("Deep Copied Classes:", classes_deep_copy)