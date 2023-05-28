#Student IDs:
#Ailan Hernandez: 862267773
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 862132856
#Malina Martinez: 862311483

#from numba import njit
import random
import pandas as pd
import math
import numpy as np

#@njit

class Classifier:
    def train(self, training_data_loc):
        #used https://www.geeksforgeeks.org/how-to-read-text-files-with-pandas/ for the following line
        training = pd.read_csv(training_data_loc, delimiter='\s{1,2}', header=None, engine='python', skipinitialspace=True)
        training = training.rename(columns={0: "label"})
        return training

    def test(self, instance, features, training):
        min_dist = math.inf
        label = None

        temp_columns = ['label']
        for feature in features:
            temp_columns.append(feature)
        temp_training = training[temp_columns] #training[temp_columns] = training[label, 1, 2, 3] for example
        temp_instance = [] #[1,2,3] == [0,1,2]
        for feature in features:
            temp_instance.append(instance[feature-1])
        
        for _, item in temp_training.iterrows():
            distance = self.compute_euclidean_distance(np.array(item), temp_instance)
            if distance < min_dist:
                min_dist = distance
                label = item['label']

        return label

    def compute_euclidean_distance(self, test_features, instance_features):
        temp_dist = 0.0
        test_features = test_features[1:]
        for i in range(len(test_features)):
            temp_dist += (float(test_features[i]) - instance_features[i])**2
        return math.sqrt(temp_dist)


def leave_one_out_cross_validation(data, current_features, feature_to_add):
    #For right now, returns a random number
    rand = round(random.uniform(0, 100), 2)
    return rand

def forward_selection(num_features, data):
    print("\nBeginning search\n")
    features = []
    best_accuracy = leave_one_out_cross_validation(data, features, 0)
    final_features = []

    print("Using no features and \"random\" evaluation, we get an accuracy of ", best_accuracy, "%\n")

    without_labels = data.drop(columns=['label'])
    for i in range(num_features):
        best_feature = None
        best_accuracy_in_loop = 0.0
        for k in without_labels.columns:
            if k not in features:
                features.append(k)
                accuracy = leave_one_out_cross_validation(data, features, k)
                print(" Using feature(s) ", str(features), " accuracy is ", accuracy, "%")
                features.remove(k)

                if accuracy > best_accuracy_in_loop:
                    best_accuracy_in_loop = accuracy
                    best_feature = k

        features.append(best_feature)

        print("\nFeature set ", str(features), " was best with an accuracy of ", best_accuracy_in_loop, "%")
        if best_accuracy_in_loop > best_accuracy:
                    best_accuracy = best_accuracy_in_loop
                    final_features = features.copy()
        elif best_accuracy_in_loop < best_accuracy:
            print("(Warning. Accuracy has decreased!)")

    print("\nFinished search!! The best subset is ", str(final_features), ", which has an accuracy of ", best_accuracy, "%")

def backward_selection(data):
    print("Beginning search")
    currFeatures = []
    for i in range(data):
        currFeatures.append(i+1)

    accuracy=leave_one_out_cross_validation(1,1,1)
    print("\nWithout removing features, Feature set "+str(currFeatures)+ " accuracy is "+str(accuracy)+"%")
    highestAccuracy=accuracy
    bestFeatures=currFeatures.copy()
    
    for i in range(data-1):
        print("")

        lowestAccuracy=101
        for j in range(len(currFeatures)):
            accuracy=leave_one_out_cross_validation(1,1,1)
            print(" Removing feature(s) {"+str(currFeatures[j])+"} accuracy is "+str(accuracy)+"%")
            if(accuracy<lowestAccuracy):
                lowestAccuracy=accuracy
                lowestAccuracyPos=j
            elif(accuracy>highestAccuracy):
                highestAccuracy=accuracy
                highestAccuracyPos=j
                bestFeatures=currFeatures.copy()
                bestFeatures.pop(highestAccuracyPos)
        currFeatures.pop(lowestAccuracyPos)
        print("\nFeature set "+str(currFeatures)+" was the worst, accuracy is "+str(lowestAccuracy)+"%")

        if highestAccuracy > accuracy:
            print("(Warning. Accuracy has decreased!)")


    print("\nFinished search!! The best subset is "+str(bestFeatures)+", which has an accuracy of "+str(highestAccuracy)+"%")
    

#reads a made up data file for right now
# data = pd.read_csv('data.txt', delimiter=' ', header=None) #this somehow still works with txt files lol
# data = data.rename(columns={0: "label"})

# print("Welcome to our Feature Selection Algorithm!\n")
# inp = input("Please enter the total number of features: ")
# print("\n1. Forward Selection")
# print("2. Backward Selection")
# algorithm_selection = input("\nPlease select an algorithm to run: ")

# if algorithm_selection == "1":
#     forward_selection(int(inp), data)

# else:
#     #backward_selection(data)
#     backward_selection(int(inp))

#2.0000000e+000  3.7256854e+000  1.8995100e+000  4.0813166e+000  1.8676158e+000  3.2975607e+000  1.0805679e+000  2.7805422e+000  4.3284038e+000  2.7017165e+000  4.7808253e+000

classify = Classifier()
training_set = classify.train('small-test-dataset.txt')
testing_instance = [3.7256855e+000,  1.8995100e+000,  4.0813166e+000,  1.8676158e+000,  3.2975607e+000,  1.0805679e+000,  2.7805422e+000,  4.3284038e+000,  2.7017165e+000,  4.7808253e+000]
features = [1, 2, 3]
classification = classify.test(testing_instance, features, training_set)
print(classification)