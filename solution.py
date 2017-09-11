import csv
import sys
import math
from collections import defaultdict
from numbers import Number

def read_file():
    with open(sys.argv[1], 'rt') as f:
        alpha = sys.argv[3]
        reader = csv.reader(f)
        featureName_list = next(reader)
        featureName_featureVal_targetVal = {}
        index_featureName = {}
        target_featureName = sys.argv[2]
        target_featureName_index = 0
        i = 0
        for featureName in featureName_list:
            if featureName not in featureName_featureVal_targetVal and featureName != target_featureName:
                featureName_featureVal_targetVal[featureName] = {}
            index_featureName[i] = featureName
            if featureName == target_featureName:
                target_featureName_index = i
            i += 1

        targetVal_freq = defaultdict(lambda: 0)
        total_targetVal = 0
        featureName_targetVal_featureValList = {}
        digit_featureNames = set()
        non_digit_featureNames = set()

        for row in reader:
            for j, val in enumerate(row):
                if j != target_featureName_index:
                    if val not in featureName_featureVal_targetVal[index_featureName[j]]:
                        featureName_featureVal_targetVal[index_featureName[j]][val] = {}
                    if row[target_featureName_index] not in featureName_featureVal_targetVal[index_featureName[j]][val]:
                        featureName_featureVal_targetVal[index_featureName[j]][val][row[target_featureName_index]] = 1
                    else:
                        featureName_featureVal_targetVal[index_featureName[j]][val][row[target_featureName_index]] += 1

                    if val.isdigit():
                        if index_featureName[j] not in featureName_targetVal_featureValList:
                            featureName_targetVal_featureValList[index_featureName[j]] = {}
                        if row[target_featureName_index] not in featureName_targetVal_featureValList[index_featureName[j]]:
                            featureName_targetVal_featureValList[index_featureName[j]][row[target_featureName_index]] = []
                        featureName_targetVal_featureValList[index_featureName[j]][row[target_featureName_index]].append(val)
                        digit_featureNames.add(index_featureName[j])
                    else:
                        non_digit_featureNames.add(index_featureName[j])
                else:
                    # targetVale
                    targetVal_freq[val] += 1
                    total_targetVal += 1

        # print(featureName_featureVal_targetVal)
        # {'outlook': {'sunny': {'no': 3, 'yes': 2}, 'overcast': {'yes': 4}, 'rainy': {'no': 2, 'yes': 3}},
        # 'windy': {'TRUE': {'no': 3, 'yes': 3}, 'FALSE': {'no': 2, 'yes': 6}},
        # 'humidity': {'75': {'yes': 1}, '70': {'no': 1, 'yes': 2}, '80': {'yes': 2}, '95': {'no': 1},
        # '86': {'yes': 1}, '90': {'no': 1, 'yes': 1}, '85': {'no': 1}, '65': {'yes': 1}, '96': {'yes': 1},
        # '91': {'no': 1}}, 'temp': {'70': {'yes': 1}, '64': {'yes': 1}, '72': {'no': 1, 'yes': 1},
        # '69': {'yes': 1}, '71': {'no': 1}, '83': {'yes': 1}, '80': {'no': 1}, '81': {'yes': 1},
        # '75': {'yes': 2}, '85': {'no': 1}, '65': {'no': 1}, '68': {'yes': 1}}}

        # print(featureName_targetVal_featureValList)
        # {'humidity': {'no': ['85', '90', '70', '95', '91'], 'yes': ['86', '96', '80', '65', '70', '80', '70', '90', '75']},
        # 'temp': {'no': ['85', '80', '65', '72', '71'], 'yes': ['83', '70', '68', '64', '69', '75', '75', '72', '81']}}
        
        # print(targetVal_freq)


        for targetVal in targetVal_freq:
            print('P(' + targetVal + ';alpha=' + str(alpha) + ')=' + str(targetVal_freq[targetVal]/total_targetVal))

        printed_already = set()

        for featureName in featureName_featureVal_targetVal:
            for featureVal in featureName_featureVal_targetVal[featureName]:
                for targetVal in featureName_featureVal_targetVal[featureName][featureVal]:
                    if not featureVal.isdigit():
                        print('P(' + featureName + '=' + featureVal + '|' + targetVal + ';alpha=' + str(alpha) + ') = '
                         + str(featureName_featureVal_targetVal[featureName][featureVal][targetVal]/targetVal_freq[targetVal]))
                            
                    else:
                        if featureName+targetVal not in printed_already:
                            printed_already.add(featureName+targetVal)
                            avg = mean(featureName_targetVal_featureValList[featureName][targetVal])
                            sd = stdev(featureName_targetVal_featureValList[featureName][targetVal])
                            print('P(' + featureName + '|' + targetVal + ';alpha=' + str(alpha) + ') = N(mean='
                             + str(avg) + ', sd=' + str(sd) + ')')

        print('Input')
        # print(featureName_featureVal_targetVal)
        for targetVal in targetVal_freq:
            p_target = targetVal_freq[targetVal]/total_targetVal
            print('P(' + targetVal + ';alpha=' + str(alpha) + ')=' + str(p_target))
            for featureName in non_digit_featureNames:
                for featureVal in featureName_featureVal_targetVal[featureName]:
                    if targetVal not in featureName_featureVal_targetVal[featureName][featureVal]:
                        print('needs smoothing')
                    else:
                        print('P(' + featureName + '=' + featureVal + '|' + targetVal + ';alpha=' + str(alpha) + ') = '
                         + str(featureName_featureVal_targetVal[featureName][featureVal][targetVal]/targetVal_freq[targetVal]))


def mean(data):
    data = list(map(int, data))
    n = len(data)
    return sum(data)/n

def stdev(data):
    data = list(map(int, data))
    n = len(data)
    c = mean(data)
    ss = sum((x-c)**2 for x in data) / (n-1)
    return ss**0.5

def mleEsimate(x, mean, std):
    coefficient = 1.0 / (math.sqrt(2*math.pi) * std)
    base = math.e
    exponent = -1.0 * (math.pow((x-mean), 2)) / (2 * math.pow(std, 2))
    return 1.0 * coefficient * (base ** exponent)

read_file()