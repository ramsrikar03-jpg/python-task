import numpy as np
marks = np.array([
    [70, 80, 90],
    [60, 75, 85],
    [50, 65, 70],
    [90, 95, 85],
    [40, 55, 60]])
total_marks = marks.sum(axis=1)
class_average = total_marks.mean()
above_average_indices = np.where(total_marks > class_average)[0]