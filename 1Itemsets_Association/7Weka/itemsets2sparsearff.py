import sys

def parse(path):
    readDat(path)

def readDat(path):
    dataRes = []
    # The maxVal would be the number of attributes
    maxVal = -1
    with open(path, 'rt') as f:
        data = f.readlines()
        for row in data:
            row = row.replace('\n', '')
            # Remove the duplicates
            temp = set()
            for i, featureVal in enumerate(row.split()):
                pos = int(featureVal)
                if pos > maxVal:
                    maxVal = pos
                temp.add(pos-1)
            # Have to sort the index
            temp = sorted(temp)
            addOneLst = []
            for i in temp:
                addOneLst.append(str(i) + ' 1')
            dataRowFormat = '{}{}{}'.format('{', ', '.join(addOneLst), '}')
            dataRes.append(dataRowFormat)

    finalRes = ['@RELATION test']
    for i in range(maxVal):
        finalRes.append('@ATTRIBUTE i{} {{0, 1}}'.format(i+1))
    finalRes.append('@DATA')
    finalRes += dataRes
    finalResStr = '\n'.join(finalRes)
    print(finalResStr)

if __name__ == '__main__':
    parse(sys.argv[1])