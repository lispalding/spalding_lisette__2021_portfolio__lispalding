# MADE BY: Lisette Spalding
# FILE NAME: main.py
# PROJECT NAME: machine_learning_experiment__pytorch
# DATE CREATED: 04/29/2021
# DATE LAST MODIFIED: 04/30/2021
# PYTHON VER. USED: 3.x

############################## IMPORTS ##############################
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle

import matplotlib.pyplot as plt
from matplotlib import style
import pickle

from os import path
################################ FIN ################################

############################ FOLDER SETUP ############################
generalFolder = path.dirname(__file__) # General folder set-up
dataFolder = path.join(generalFolder, "data_sets")
dataSet = path.join(dataFolder, "student-mat.csv")
################################ FIN ################################

############################# DATA SETUP #############################
## Collecting and loading data:
data = pd.read_csv(dataSet, sep = ";") # Since our data is separated with semicolons we need to use this: sep = ";"
print(data.head())

data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]] # Collecting only the relevant data from the data set
data = shuffle(data) # Optional -- Shuffling the data
## Data collection and loading FIN

## Separating the data:
predict = "G3"

x = np.array(data.drop([predict], 1)) # Features
y = np.array(data[predict]) # Labels
## Separating the data FIN

xTrain, xTest, yTrain, yTest = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)
################################ FIN ################################

############################# ALGORITHM #############################

################ TESTING CODE ################
# linear = linear_model.LinearRegression() # Defining the linear model that will be used
#
# linear.fit(xTrain, yTrain)
# accuracy = linear.score(x_test, y_test)
#
# print(accuracy) # Checking how well the algorithm preformed on the test
#
# ## Viewing Constants:
# print("Coefficient: \n", linear.coef_) # These are each slope value
# print("Intercept: \n", linear.intercept_) # This is the intercept
# ## Constants FIN
#
# predictions = linear.predict(xTest) # Gets a list of all predictions
#
# for x in range(len(predictions)):
#     print(predictions[x], xTest[x], yTest[x])
################ TESTING FIN #################

## Training the model multiple times for best possible score
best = 0
for _ in range(20):
    xTrain, xTest, yTrain, yTest = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

    linear = linear_model.LinearRegression() # Defining the linear model taht will be used

    linear.fit(xTrain, yTrain)
    accuracy = linear.score(xTest, yTest)

    print("Accuracy: " + str(accuracy))

    if accuracy > best:
        best = accuracy
        with open("studentgrades.pickle", "wb") as f:
            pickle.dump(linear, f)

## Loading Model
pickleIn = open("studentgrades.pickle", "rb")
linear = pickle.load(pickleIn)

print("-------------------------")
print('Coefficient: \n', linear.coef_)
print('Intercept: \n', linear.intercept_)
print("-------------------------")

predicted = linear.predict(xTest)

for x in range(len(predicted)):
    print(predicted[x], xTest[x], yTest[x])

## Drawing and plotting the model
plot = "failures"

plt.scatter(data[plot], data["G3"])
plt.legend(loc = 4)
plt.xlabel(plot)
plt.ylabel("Final Grade")

plt.show()
################################ FIN ################################
