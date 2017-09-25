import sys

def parse(path):
    readDat(path)

def readDat(path):
    dataRes = []
    maxVal = -1
    with open(path, 'rt') as f:
        data = f.readlines()
        for row in data:
            row = row.replace('\n', '')
            temp = []
            for i, featureVal in enumerate(row.split()):
                pos = int(featureVal)
                if pos > maxVal:
                    maxVal = pos
                temp.append(pos-1)
                # temp.append(str(pos-1) + ' 1')
            temp = sorted(temp)
            addOneLst = []
            for i in temp:
                addOneLst.append(str(i) + ' 1')
            dataRowFormat = '{}{}{}'.format('{', ', '.join(addOneLst), '}')
            # dataRowFormat = '{}{}{}'.format('{', ', '.join(temp), '}')
            dataRes.append(dataRowFormat)

    finalRes = ['@RELATION test']
    for i in range(maxVal):
        finalRes.append('@ATTRIBUTE i' + str(i+1) + ' {0, 1}')
    finalRes.append('@DATA')
    finalRes += dataRes
    finalResStr = '\n'.join(finalRes)
    print(finalResStr)

if __name__ == '__main__':
    parse(sys.argv[1])