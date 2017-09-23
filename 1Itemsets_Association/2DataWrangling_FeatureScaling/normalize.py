import sys
import collections

featureIndex_val = collections.OrderedDict()
originalData = []
normalizedData = []

def normalize(path, low, high, numOfDigits):
    readTxt(path)
    computeNormalizedData(low, high, numOfDigits)
    writeTxt(low, high, numOfDigits)

def readTxt(path):
    with open(path, 'rt') as f:
        data = f.readlines()
        for row in data:
            temp = []
            for i, featureVal in enumerate(row.split()):
                temp.append(featureVal)
                if i not in featureIndex_val:
                    featureIndex_val[i] = [featureVal]
                else:
                    featureIndex_val[i].append(featureVal)
            originalData.append(temp)

def computeNormalizedData(low, high, numOfDigits):
    for rowIndex, row in enumerate(originalData):
        temp = []
        for colIndex, curVal in enumerate(row):
            temp.append(rescale(high, low, max(featureIndex_val[colIndex]), min(featureIndex_val[colIndex]), curVal, numOfDigits))
        normalizedData.append(temp)

def rescale(max_new, min_new, max_old, min_old, cur, numOfDigits):
    res = (float(max_new) - float(min_new)) / (float(max_old) - float(min_old)) * (float(cur) - float(max_old)) + float(max_new)
    digits = '%.' + numOfDigits + 'f'
    res = digits % res
    return res

def writeTxt(low, high, numOfDigits):
    path = '2_out_{}_{}_{}.txt'.format(low, high, numOfDigits)
    with open(path, 'w') as f:
        for normalizedValRow in normalizedData:
            print(' '.join(normalizedValRow), file=f)

if __name__ == '__main__':
    normalize(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])