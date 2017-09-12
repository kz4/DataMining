import csv
import sys
import math
from collections import defaultdict
from numbers import Number

alpha = -1
featureName_featureVal_targetVal = {}
index_featureName = {}
targetVal_freq = defaultdict(lambda: 0)
featureName_targetVal_featureValList = {}
digit_featureNames = set()
non_digit_featureNames = set()
targetValSet = set()
featureName_featureVal_targetVal_smoothing_lst = []
featureVal_underCondition_targetVal = {}
inputs = []
inputDict = {}

def read_file():
    with open(sys.argv[1], 'rt') as f:
        target_featureName = sys.argv[2]
        alpha = sys.argv[3]
        inputs, inputDict = readInputArgv()
        reader = csv.reader(f)
        featureName_list = next(reader)
        
        target_featureName_index = processFeatureNameList(featureName_list, target_featureName)

        total_targetVal = processFeatureValueData(reader, target_featureName_index)

        featureName_featureVal_targetVal_smoothing_lst = findSmoothingFeatures()

        printTargetValProbability(total_targetVal)
        
        printed_already = set()

        # print probability except the ones that need smoothing
        for featureName in featureName_featureVal_targetVal:
            for featureVal in featureName_featureVal_targetVal[featureName]:
                for targetVal in featureName_featureVal_targetVal[featureName][featureVal]:
                    if not featureVal.isdigit():
                        if [featureName, featureVal, targetVal] not in featureName_featureVal_targetVal_smoothing_lst:
                            # no need to smooth
                            v = featureName_featureVal_targetVal[featureName][featureVal][targetVal] / targetVal_freq[targetVal]
                            print('P(' + featureName + '=' + featureVal + '|' + targetVal + ';alpha=' + str(alpha) + ') = '
                             + str(v))
                            if targetVal not in featureVal_underCondition_targetVal:
                                featureVal_underCondition_targetVal[targetVal] = {}
                                featureVal_underCondition_targetVal[targetVal][featureVal] = v
                            else:
                                featureVal_underCondition_targetVal[targetVal][featureVal] = v
                    else:
                        if featureName+targetVal not in printed_already:
                            printed_already.add(featureName+targetVal)
                            avg = mean(featureName_targetVal_featureValList[featureName][targetVal])
                            sd = stdev(featureName_targetVal_featureValList[featureName][targetVal])
                            print('P(' + featureName + '|' + targetVal + ';alpha=' + str(alpha) + ') = N(mean='
                             + str(avg) + ', sd=' + str(sd) + ')')

        # print smoothing probability
        for [featureName, featureVal, targetVal] in featureName_featureVal_targetVal_smoothing_lst:
            nu = 0
            if targetVal not in featureName_featureVal_targetVal[featureName][featureVal]:
                nu = int(alpha)
            else:
                nu = (featureName_featureVal_targetVal[featureName][featureVal][targetVal] + int(alpha))
            de = (targetVal_freq[targetVal]) + int(alpha) * len(featureName_featureVal_targetVal[featureName].keys())
            v = nu / de
            print('P(' + featureName + '=' + featureVal + '|' + targetVal + ';alpha=' + str(alpha) + ') = '
             + str(v))
            if targetVal not in featureVal_underCondition_targetVal:
                featureVal_underCondition_targetVal[targetVal] = {}
                featureVal_underCondition_targetVal[targetVal][featureVal] = v
            else:
                featureVal_underCondition_targetVal[targetVal][featureVal] = v

        for targetVal in targetValSet:
            for j, inp in inputDict.items():
                if inp.isdigit():
                    avg = mean(featureName_targetVal_featureValList[featureName_list[j]][targetVal])
                    sd = stdev(featureName_targetVal_featureValList[featureName_list[j]][targetVal])
                    mle = mleEsimate(int(inp), avg, sd)
                    featureVal_underCondition_targetVal[targetVal][inp] = mle

        print('Input: ', inputs)

        computeXUnderConditionTargetVal(total_targetVal, featureName_list)

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

def processFeatureNameList(featureName_list, target_featureName):
    i = 0
    for featureName in featureName_list:
        if featureName not in featureName_featureVal_targetVal and featureName != target_featureName:
            featureName_featureVal_targetVal[featureName] = {}
        index_featureName[i] = featureName
        if featureName == target_featureName:
            target_featureName_index = i
        i += 1
    return target_featureName_index

def processFeatureValueData(reader, target_featureName_index):
    total_targetVal = 0
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
                targetValSet.add(val)
    return total_targetVal

def findSmoothingFeatures():
    for featureName in featureName_featureVal_targetVal:
        if featureName in non_digit_featureNames:
            for featureVal in featureName_featureVal_targetVal[featureName]:
                for targetVal in targetValSet:
                    if targetVal not in featureName_featureVal_targetVal[featureName][featureVal]:
                        featureName_featureVal_targetVal_smoothing_lst.append([featureName, featureVal, targetVal])

    for [featureName, featureVal, targetVal] in featureName_featureVal_targetVal_smoothing_lst:
        for featureVal in featureName_featureVal_targetVal[featureName]:
            if [featureName, featureVal, targetVal] not in featureName_featureVal_targetVal_smoothing_lst:
                featureName_featureVal_targetVal_smoothing_lst.append([featureName, featureVal, targetVal])
    return featureName_featureVal_targetVal_smoothing_lst

def printTargetValProbability(total_targetVal):
    for targetVal in targetVal_freq:
        print('P(' + targetVal + ';alpha=' + str(alpha) + ')=' + str(targetVal_freq[targetVal]/total_targetVal))

def readInputArgv():
    i = 4
    while i < len(sys.argv):
        inputs.append(sys.argv[i])
        inputDict[i-4] = sys.argv[i]
        i += 1
    return inputs, inputDict

def computeXUnderConditionTargetVal(total_targetVal, featureName_list):
    for targetVal in targetVal_freq:
        p_target = targetVal_freq[targetVal]/total_targetVal
        print('P(' + targetVal + ';alpha=' + str(alpha) + ')=' + str(p_target))
        for i, featureVal in inputDict.items():
            v = featureVal_underCondition_targetVal[targetVal][featureVal]
            print('P(' + featureName_list[i] + '=' + featureVal + '|' + targetVal + ';alpha=' + str(alpha) + ') = '
             + str(v))

read_file()