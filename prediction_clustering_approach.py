from gather_data import read_twitter_data
from models import vocabulary
from math import fabs
import sys
import plot_helper

'''
    This build the distance between the word measured by the distance (characters)
    in the string that represents the tweet. This turns out into A LOT of words and thus
    the graph becomes laaaaaaaaaarge.
'''
def build_distance(data):
	ignore = set(['.',',',':','"'])
	all_words = set()
	for t in data:
		text = t['text']
		arr = text.split(" ")
		for word in arr:
			all_words.add(word)

	distance = {}
	max_distance = 300
	for w1 in all_words:
		for w2 in all_words:
			if w1 not in distance: distance[w1] = {}
			if w2 not in distance: distance[w2] = {}
			if w1 != w2:
				distance[w1][w2] = max_distance
				distance[w2][w1] = max_distance

	
	for t in data:
		text = t['text']
		arr = text.split(" ")
		for i,word1 in enumerate(arr):
			for j,word2 in enumerate(arr):
				if word1 != word2:
					d = min(distance[word1][word2],fabs(i-j))
					distance[word1][word2] = d
					distance[word2][word1] = d
			
	return distance

#Just a hack to use properly thd MDS algorithm...
#Transform the original graph into a adjacency matrix with numerical indices and array-based.
def build_adjacency_matrix(adj):
    
    keys = adj.keys()
    size = len(keys)
    m2 = []
    for u in range(0,size):
            row = []
            for v in range(0,size):
                    if u != v:
                            row.append(adj[keys[u]][keys[v]])
                    else:
                            row.append(0)

            m2.append(row)

    print "finish setting up the matrix"
    return m2
    


data = read_twitter_data("../tweets.csv",100) #threshold on maximum tweets, > 500 gets slower due to there is a lot of words.
                                             #That should be improved somehow in order to visualize data in a better way.
print "finish reading data"
adj =  build_distance(data)
print "finish building distance"
matrix = build_adjacency_matrix(adj)
plot_helper.plot(matrix) 


