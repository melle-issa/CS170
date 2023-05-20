#Student IDs:
#Ailan Hernandez: 862267773
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 862132856
#Malina Martinez: 862311483

#from numba import njit
import random
import pandas as pd

#@njit

def leave_one_out_cross_validation(data, current_features, feature_to_add):
    #For right now, returns a random number
    rand = round(random.uniform(0, 100), 2)
    return rand

def forward_selection(data):
    print("Beginning search")
    features = []
    without_labels = data.drop(columns=['label'])
    for i in range(len(without_labels.columns) - 1):
        best_feature = None
        best_accuracy = 0.0
        for k in without_labels.columns[:-1]:
            if k not in features:
                features.append(k)
                accuracy = leave_one_out_cross_validation(data, features, k)
                print("Using feature(s) ", features, " accuracy is ", accuracy, "%")
                features.remove(k)

                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_feature = k

        features.append(best_feature)
        print("Feature set ", features, " was best with an accuracy of ", best_accuracy, "%")

def backward_selection(data):
    print("Beginning search")
    features = []
    without_labels = data.drop(data["label"])

#reads a made up data file for right now
data = pd.read_csv('data.txt', delimiter=' ', header=None) #this somehow still works with txt files lol
data = data.rename(columns={0: "label"})

print("Welcome to our Feature Selection Algorithm!")
inp = input("Please enter the total number of features: ")
print("1. Forward Selection")
print("2. Backward Selection")
algorithm_selection = input("Please select an algorithm to run: ")

if algorithm_selection == "1":
    forward_selection(data)

else:
    backward_selection(data)
