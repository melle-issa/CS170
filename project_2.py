#Student IDs:
#Ailan Hernandez: 862267773
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 862132856
#Malina Martinez: 862311483

import pandas as pd
import math
import numpy as np

class Classifier:
    # used https://stackoverflow.com/questions/26414913/normalize-columns-of-a-dataframe for this function
    def normalize_data(self, data):
        normalized_data = (data - data.min()) / (data.max() - data.min())
        return normalized_data
    
    def train(self, training_data_loc):
        #used https://www.geeksforgeeks.org/how-to-read-text-files-with-pandas/ for the following line
        training = pd.read_csv(training_data_loc, delimiter='\s{1,2}', header=None, engine='python', skipinitialspace=True)
        training = training.rename(columns={0: "label"})

        normalized_training = self.normalize_data(training.drop(columns=['label']))
        normalized_training['label'] = training['label']
        columns = list(normalized_training.columns)
        column_index = columns.index('label')
        columns = [columns[column_index]] + columns[:column_index] + columns[column_index+1:]
        return_df = normalized_training[columns]
        return return_df

    def test(self, instance, features, training):
        min_dist = math.inf
        label = None

        temp_columns = ['label']
        for feature in features:
            temp_columns.append(feature)
        temp_training = training[temp_columns] #training[temp_columns] = training[label, 1, 2, 3] for example
        temp_instance = [] #[1,2,3] == [0,1,2]
        for feature in features:
            #temp_instance.append(instance[feature-1])
            temp_instance.append(instance[feature])
        
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


class Validator:
    def leave_one_out_validation(self, data, features):
        numCorrect=0
        for i in range(len(data)):
            testingData=data.copy()
            testing_instance=testingData.iloc[i].values
            testingData = testingData.drop(testingData.index[i])
            classificationTest = Classifier().test(testing_instance, features, testingData)
            classificationActual = Classifier().test(testing_instance, features, data)
            if(classificationActual==classificationTest):
                numCorrect=numCorrect+1
        return numCorrect/(len(data))
            

def forward_selection(num_features, training_set):
    data = training_set.copy()
    print("\nBeginning search\n")
    features = []
    best_accuracy = 0.0
    final_features = []

    without_labels = data.drop(columns=['label'])
    for i in range(num_features):
        best_feature = None
        best_accuracy_in_loop = 0.0
        for k in without_labels.columns:
            if k not in features:
                features.append(k)
                accuracy = Validator().leave_one_out_validation(data, features)
                print(" Using feature(s) ", str(features), " accuracy is ", accuracy*100, "%")
                features.remove(k)

                if accuracy > best_accuracy_in_loop:
                    best_accuracy_in_loop = accuracy
                    best_feature = k

        features.append(best_feature)

        print("\nFeature set ", str(features), " was best with an accuracy of ", best_accuracy_in_loop*100, "%")
        if best_accuracy_in_loop > best_accuracy:
                    best_accuracy = best_accuracy_in_loop
                    final_features = features.copy()
        elif best_accuracy_in_loop < best_accuracy:
            print("(Warning. Accuracy has decreased!)")

    print("\nFinished search!! The best subset is ", str(final_features), ", which has an accuracy of ", best_accuracy*100, "%")

def backward_elimination(data, training_set):
    training_copy = training_set.copy()
    print("Beginning search")
    currFeatures = []
    for i in range(data):
        currFeatures.append(i+1)

    accuracy=Validator().leave_one_out_validation(training_copy, currFeatures)
    print("\nWithout removing features, Feature set "+str(currFeatures)+ " accuracy is ", accuracy * 100, "%")
    highestAccuracy=accuracy
    bestFeatures=currFeatures.copy()
    
    for i in range(data-1):
        print("")

        lowestAccuracy=101
        for j in range(len(currFeatures)):
            features_without_j = currFeatures[:j] + currFeatures[j+1:]
            accuracy = Validator().leave_one_out_validation(training_copy, features_without_j)
            print(" Removing feature(s) {"+str(currFeatures[j])+"} accuracy is ", accuracy * 100, "%")
            if(accuracy<lowestAccuracy):
                lowestAccuracy=accuracy
                lowestAccuracyPos=j
            elif(accuracy>highestAccuracy):
                highestAccuracy=accuracy
                highestAccuracyPos=j
                bestFeatures=currFeatures.copy()
                bestFeatures.pop(highestAccuracyPos)
        currFeatures.pop(lowestAccuracyPos)
        print("\nFeature set "+str(currFeatures)+" was the worst, accuracy is ", lowestAccuracy * 100, "%")

        if highestAccuracy > accuracy:
            print("(Warning. Accuracy has decreased!)")


    print("\nFinished search!! The best subset is "+str(bestFeatures)+", which has an accuracy of ", highestAccuracy * 100, "%")
    


print("Welcome to our Feature Selection Algorithm!\n")
inp = "Small_data__52.txt" #input("Please enter the name of the text file (include extension): ")

data = Classifier().train(inp)

print("\n1. Forward Selection")
print("2. Backward Elimination")
algorithm_selection = input("\nPlease select an algorithm to run: ")

num_features = len(data.columns) - 1

if algorithm_selection == "1":
    forward_selection(num_features, data)

else:
    backward_elimination(num_features, data)
