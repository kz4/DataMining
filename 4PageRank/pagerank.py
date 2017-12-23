import sys
from collections import defaultdict

path = 'wt2g_inlinks.txt'
link_inlinks = {}
link_outlinkcount = defaultdict(int)
all_links = set()
sink_links = set()
link_score = {}
link_score_previous = {}
link_damping = 0.85

def readfile():
    with open(path, 'rt') as f:
        data = f.readlines()
        i = 0
        for row in data:
            links = row.split()

            link = links[0]
            link_inlinks[link] = set(links[1:])
            all_links.add(link)
            for link in link_inlinks[link]:
                all_links.add(link)
            for l in links[1:]:
                link_outlinkcount[l] += 1 
            
            i += 1
            
            # if i == 5:
            #     break

def retrieve_sinklinks():
    outLinks = link_outlinkcount.keys();
    for link in [link for link in link_inlinks.keys() if link not in outLinks]:
        sink_links.add(link)

def is_converged(counter):    
    if counter == 1:
        return False
    tot = sum([(link_score[link] - link_score_previous[link])**2 for link in link_score.keys()])**(1/2)
    return tot <= 10 ** (-5)

def calculate_pagerank():
    link_size = len(all_links)
    # Initialize all the score to 1/n
    link_score = { link : 1 / link_size for link in all_links }

    # all_links might miss a couple links
    for link in link_inlinks.keys():
        for inlink in link_inlinks[link]:
            link_score[inlink] = 1 / link_size

    counter = 1
    while not is_converged(counter):
        link_score_previous = link_score
        sinkPR = sum([link_score[link] for link in link_score.keys()])
        newPR = {}
        for link in all_links:
            newPR[link] = (1 - link_damping) / link_size + link_damping * sinkPR / link_size
            for inlink in link_inlinks[link]:
                newPR[link] += link_damping * link_score[inlink] / link_outlinkcount[inlink]
        sum_score = sum(newPR.values())
        link_score = { link : newPR[link] / sum_score for link in newPR.keys() }
                
        counter += 1
        if counter == 100:
            break


readfile()
retrieve_sinklinks()
calculate_pagerank()