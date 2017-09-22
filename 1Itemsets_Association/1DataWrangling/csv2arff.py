import sys
import csv
import collections

featureName_featureVal_freq = {}
index_featureName = collections.OrderedDict()
data = []
featureNameThatAreDigit = set()

def csvToarff(path):
    featureName_featureVal_freq = readCsv(path)
    writeArff(path)

def readCsv(path):
    with open(path, 'rt') as f:
        reader = csv.reader(f)
        featureName_list = next(reader)
        for i, featureName in enumerate(featureName_list):
            featureName_featureVal_freq[featureName] = {}
            index_featureName[i] = featureName

        for row in reader:
            dataRow = []
            for j, val in enumerate(row):
                featureName = index_featureName[j]
                if not val:
                    dataRow.append('?')
                    continue
                if val.isdigit():
                    featureNameThatAreDigit.add(featureName)
                if val not in featureName_featureVal_freq[featureName]:
                    featureName_featureVal_freq[featureName][val] = 1
                else:
                    featureName_featureVal_freq[featureName][val] += 1
                dataRow.append(val)
            data.append(dataRow)

def writeArff(path):
    res = []
    res.append('@relation ' + path)

    for i, featureName in index_featureName.items():
        if featureName not in featureNameThatAreDigit:
            res.append('@attribute ' + featureName + ' {' + ','.join(featureName_featureVal_freq[featureName].keys()) + '}')
        else:
            res.append('@attribute ' + featureName + ' numeric')
    res.append('@data')
    res += [','.join(row) for row in data]
    print('\n'.join(res))

if __name__ == '__main__':
    csvToarff(sys.argv[1])