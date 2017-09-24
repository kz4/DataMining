import sys
import csv
import collections
import matplotlib.pyplot as plt

# Note:
# Paper = publication
# References (number of publications a publication refers to) and citations (number of publications referring to a publication)

author_publications = {}
venue_numOfPublication = {}
year_publications = {}
publication_references = {}
publication_citations = {}
references = set()
authors_venues_publications_citations = [0, 0, 0, 0]

def analyze(path):
    readTxt(path)

def readTxt(path):
    curIndex = -1
    totalDistinctPublication = 0
    totalDistinctReferences = 0
    with open(path, 'rt') as f:
        data = f.readlines()
        data = [d for d in data if d != '\n']
        for row in data:
            row = row.replace('\n', '')
            if row.startswith('#index '):
                curIndex = row[7:]
            elif row.startswith('#* '):
                totalDistinctPublication += 1
            elif row.startswith('#@ '):
                authors = row[3:].split(';')
                for au in authors:
                    if au not in author_publications:
                        author_publications[au] = [curIndex]
                    else:
                        author_publications[au].append(curIndex)
            elif row.startswith('#t '):
                year = row[3:]
                if year not in year_publications:
                    year_publications[year] = [curIndex]
                else:
                    year_publications[year].append(curIndex)
            elif row.startswith('#c '):
                venue = row[3:]
                if venue not in venue_numOfPublication:
                    venue_numOfPublication[venue] = 1
                else:
                    venue_numOfPublication[venue] += 1
            elif row.startswith('#% '):
                ref = row[3:]
                references.add(ref)
                totalDistinctReferences += 1
                if curIndex not in publication_references:
                    publication_references[curIndex] = [ref]
                else:
                    publication_references[curIndex].append(ref)
                if ref not in publication_citations:
                    publication_citations[ref] = [curIndex]
                else:
                    publication_citations[ref].append(curIndex)
            elif row.startswith('#! '):
                pass
            else:
                pass
    # print(author_publications)
    # print(venue_numOfPublication)
    # print(year_publications)
    # print(publication_references)
    # print(publication_citations)

    # 3.1a Distinct authors, publication venues, publications, and citations/references
    # totalDistinctAuthorsWithoutEmptyName = len([author for author in author_publications.keys() if author])
    print('Total distinct authors: ', len(author_publications))
    print('Total distinct venues: ', len(venue_numOfPublication))
    print('Total distinct publications: ', str(totalDistinctPublication))
    print('Total distinct citations/references: ', len(references))
    print('Total distinct citations/references: ', totalDistinctReferences)

    # Total distinct authors:  1484999
    # Total distinct venues:  255686
    # Total distinct publications:  1976815
    # Total distinct citations/references:  871089

    authors_venues_publications_citations[0] = len(author_publications)
    authors_venues_publications_citations[1] = len(venue_numOfPublication)
    authors_venues_publications_citations[2] = totalDistinctPublication
    authors_venues_publications_citations[3] = len(references)

    # 3.2a Histogram of the number of publications per author
    plt.xlabel('Number of publications')
    plt.ylabel('Count of authors')
    plt.title('Histogram of Number of publications per author')
    plt.hist([len(lstOfPublications) for lstOfPublications in author_publications.values()])
    plt.yscale('log')
    plt.show()

    # 3.2b Calculate the mean and standard deviation of the number of publications per author
    print()
    print()
    publications_per_author_lst = [len(lstOfPublications) for lstOfPublications in author_publications.values()]
    mean_publications_per_author = mean(publications_per_author_lst)
    stdev_publications_per_author = stdev(publications_per_author_lst)
    q1, q2, q3 = quartile(sorted(publications_per_author_lst))
    q1_publications_per_author = q1
    q2_publications_per_author = q2
    q3_publications_per_author = q3
    print('Mean of the number of publications per author: ', mean_publications_per_author)
    print('Standard deviation of the number of publications per author', stdev_publications_per_author)
    print('Q1 of the number of publications per author', q1_publications_per_author)
    print('Q2 of the number of publications per author', q2_publications_per_author)
    print('Q3 of the number of publications per author', q3_publications_per_author)

    # 3.2c Histogram of the number of publications per venue
    publications_per_venue_lst = [lstOfPublications for lstOfPublications in venue_numOfPublication.values()]
    plt.xlabel('Number of publications')
    plt.ylabel('Count of venue')
    plt.title('Histogram of Number of publications per venue')
    plt.hist(publications_per_venue_lst)
    plt.yscale('log')
    plt.show()

    mean_publications_per_venue = mean(publications_per_venue_lst)
    stdev_publications_per_venue = stdev(publications_per_venue_lst)
    q1, q2, q3 = quartile(sorted(publications_per_venue_lst))
    q1_publications_per_venue = q1
    q2_publications_per_venue = q2
    q3_publications_per_venue = q3
    print('Mean of the number of publications per venue: ', mean_publications_per_venue)
    print('Standard deviation of the number of publications per venue', stdev_publications_per_venue)
    print('Q1 of the number of publications per venue', q1_publications_per_venue)
    print('Q2 of the number of publications per venue', q2_publications_per_venue)
    print('Q3 of the number of publications per venue', q3_publications_per_venue)

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

def quartile(data):
    q1 = q2 = q3 = 0
    l = len(data)
    if l % 2 == 1:
        median = int(l/2)
        q2 = data[median]
        if median % 2 == 1:
            i = int(median / 2)
            q1 = data[i]
            q3 = data[int((median + l) / 2)]
        else:
            i = int(median / 2)
            j = int(median / 2 - 1)
            q1 = (data[i] + data[j]) / 2.0
            q3 = (data[int((median + l) / 2)] + data[int((median + l) / 2 + 1)]) / 2.0
    else:
        median = int(l/2)
        median2 = median - 1
        q2 = (data[median] + data[median2]) / 2.0
        if median % 2 == 1:
            i = int(median / 2)
            q1 = data[i]
            q3 = data[int((median + l) / 2)]
        else:
            i = int(median / 2)
            j = int(median / 2 - 1)
            q1 = (data[i] + data[j]) / 2.0
            q3 = (data[int((median + l) / 2)] + data[int((median + l) / 2 - 1)]) / 2.0
    return q1, q2, q3

if __name__ == '__main__':
    analyze(sys.argv[1])