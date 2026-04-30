#======================================================================
#=======================================================================
""
#Performing Linear Regression Algorithm for the quadratic equation
#X = 7a + 3b + 4c + 9d
#Using sklearn module to perform the linear regression equation.
""
#======================================================================
#======================================================================

#Importing required modules
from random import randint
from sklearn.linear_model import LinearRegression

#Constructing training dataset using Random module

#Setting up the limit and counts to generate the data
train_set_limit = 1000
train_set_count = 150

#generated trained data will be stored as list in train_input variable
train_input = list()

#generated outputs are stored here. It is learned data.
train_output = list()

#it will assign different unique values to the variables until the count is met
for i in range(train_set_count):
    a = randint(0, train_set_limit)
    b = randint(0, train_set_limit)
    c = randint(0, train_set_limit)
    d = randint(0, train_set_limit)
    op = (7*a)+(3*b)+(4*c)+(9*d)
    train_input.append([a,b,c,d])
    train_output.append(op)

#Training the model
predictor = LinearRegression(n_jobs = -1)
predictor.fit(X = train_input, y = train_output)

#Testing the model
#Sample test values
x_test = [[10,20,30,40]]
outcome = predictor.predict(X = x_test)
coefficients = predictor.coef_

#Printing the prediction
print("Outcome of given test data is: ")
print("Outcome: {} \nCoefficients: {}".format(outcome,coefficients))