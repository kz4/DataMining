import sys
import csv
import collections

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

    # 3.1a
    # totalDistinctAuthorsWithoutEmptyName = len([author for author in author_publications.keys() if author])
    print('Total distinct authors: ', len(author_publications))
    print('Total distinct venues: ', len(venue_numOfPublication))
    print('Total distinct publications: ', str(totalDistinctPublication))
    print('Total distinct citations/references: ', len(references))
    authors_venues_publications_citations[0] = len(author_publications)
    authors_venues_publications_citations[1] = len(venue_numOfPublication)
    authors_venues_publications_citations[2] = totalDistinctPublication
    authors_venues_publications_citations[3] = len(references)

if __name__ == '__main__':
    analyze(sys.argv[1])