import csv
import sys
import math
from collections import defaultdict

def read_file():
    with open(sys.argv[1], 'rt') as f:
        reader = csv.reader(f)
        featureName_list = next(reader)
        featureName_featureVal_targetVal = {}
        index_featureName = {}
        target_featureName = sys.argv[2]
        target_featureName_index = 0
        i = 0
        for featureName in featureName_list:
            if featureName not in featureName_featureVal_targetVal:
                featureName_featureVal_targetVal[featureName] = {}
            index_featureName[i] = featureName
            if featureName == target_featureName:
                target_featureName_index = i
            i += 1

        # {'outlook': {'sunny': {'no': 3, 'yes': 2}, 'overcast': {'yes': 4}, 'rainy': {'no': 2, 'yes': 3}},
        # 'windy': {'TRUE': {'no': 3, 'yes': 3}, 'FALSE': {'no': 2, 'yes': 6}},
        # 'humidity': {'75': {'yes': 1}, '70': {'no': 1, 'yes': 2}, '80': {'yes': 2}, '95': {'no': 1},
        # '86': {'yes': 1}, '90': {'no': 1, 'yes': 1}, '85': {'no': 1}, '65': {'yes': 1}, '96': {'yes': 1},
        # '91': {'no': 1}}, 'play': {}, 'temp': {'70': {'yes': 1}, '64': {'yes': 1}, '72': {'no': 1, 'yes': 1},
        # '69': {'yes': 1}, '71': {'no': 1}, '83': {'yes': 1}, '80': {'no': 1}, '81': {'yes': 1},
        # '75': {'yes': 2}, '85': {'no': 1}, '65': {'no': 1}, '68': {'yes': 1}}}
        for row in reader:
            for j, val in enumerate(row):
                if j != target_featureName_index:
                    if val not in featureName_featureVal_targetVal[index_featureName[j]]:
                        featureName_featureVal_targetVal[index_featureName[j]][val] = {}
                    if row[target_featureName_index] not in featureName_featureVal_targetVal[index_featureName[j]][val]:
                        featureName_featureVal_targetVal[index_featureName[j]][val][row[target_featureName_index]] = 1
                    else:
                        featureName_featureVal_targetVal[index_featureName[j]][val][row[target_featureName_index]] += 1
        print(featureName_featureVal_targetVal)


def mean(data):
    n = len(data)
    return sum(data)/n

def stdev(data):
    n = len(data)
    c = mean(data)
    ss = sum((x-c)**2 for x in data) / (n-1)
    return ss**0.5

def mleEsimate(x, mean, std):
    coefficient = 1.0 / (math.sqrt(2*math.pi) * std)
    base = math.e
    exponent = -1.0 * (math.pow((x-mean), 2)) / (2 * math.pow(std, 2))
    return 1.0 * coefficient * (base ** exponent)

d = [
83
,70
,68
,64
,69
,75
,75
,72
,81]

# print(mean(d)) 
# print(stdev(d)) 
read_file()
# print(mleEsimate(d, 1, 2))
# print(math.e)
# print (math.pi)