from gather_data import read_twitter_data
from models import vocabulary
from math import fabs
from models import union_find
from random import randint
from random import uniform
import sys
import plot_helper
from collections import deque

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
    return m2,keys
    
'''

'''
def single_link_clustering(distance_matrix,k):
    dsu = union_find(len(distance_matrix))
    edges = []
    i = 0
    while i < len(distance_matrix):
        j = i + 1
        while j < len(distance_matrix):
            d = distance_matrix[i][j]
            edges.append( (d,i,j) )
            j = j + 1
        i = i + 1
    
    edges.sort()
    idx = 0
    while dsu.count_components() > k:
        d,u,v = edges[idx]
        if dsu.same_component(u,v) is False:
            dsu.union(u,v)
        
        idx = idx + 1
    
    #print dsu.count_components(), len(distance_matrix)
    clusters = []
    i = 0
    while i < len(dsu.parent):
        clusters.append(dsu.find(i))
        i += 1
    return clusters

def k_means_clustering(distance_matrix,k):
    
    def trunc(f, n):
        slen = len('%.*f' % (n, f))
        return float(str(f)[:slen])
    
    x,y = plot_helper.to_x_y(distance_matrix)
    centroids = []
    i = 0
    minx = min(x)
    miny = min(y)
    maxx = max(x)
    maxy = max(y)
    while i < k:
        centroids.append( (trunc(uniform(minx,maxx),3) ,trunc(uniform(miny,maxy),3)) )
         
        i += 1
    
    
    
    def distance(x1,y1,x2,y2):
        return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)
    
    def avg(a):
        return sum(a)/len(a)
    
    def do_cluster(centroids,x_,y_):
        clusters = {}
        for j,coord in enumerate(zip(x_,y_)):
            x,y = coord
            cl = centroids[0]
            idx = 0
            for i,centroid in enumerate(centroids):
                if distance(x,y,centroid[0],centroid[1]) < distance(x,y,cl[0],cl[1]):
                    cl = (centroid[0],centroid[1])
                    idx = i
            
            if idx not in clusters:
                clusters[idx] = []
       
            clusters[idx].append(j)
        
        return clusters
    
    
    clusters = do_cluster(centroids,x,y)
    while True:
        new_centroids = [0]*len(centroids)
        for i in clusters:
            xx,yy = 0,0
            for idx in clusters[i]:
                xx += x[idx]
                yy += y[idx]
            
            xx = trunc(xx / len(clusters[i]),3)
            yy = trunc(yy / len(clusters[i]),3)
            
            new_centroids[i] = xx,yy
        
        if (new_centroids) == (new_centroids):
            break
        clusters = do_cluster(centroid,x,y)
    
    
    clusters_array = [0]*len(x)
    for idx in clusters:
        for i in clusters[idx]:
            clusters_array[i] = idx
    
    print len(clusters)
    return clusters_array
    
    
        
    
def build_colors(clusters):
    idxs = set(clusters)
    for i in idxs:
        color = randint(0,len(clusters)**3)
        clusters = [color if x==i else x for x in clusters]
    
    return clusters

def test_with_twitter_data():
    max_tweets = 100
    data = read_twitter_data("../tweets.csv",max_tweets) #threshold on maximum tweets, > 500 gets slower due to there is a lot of words.
                                                 #That should be improved somehow in order to visualize data in a better way.
    print "finish reading data"
    adj =  build_distance(data)
    print "finish building distance"
    matrix,labels = build_adjacency_matrix(adj)
    k = 10
    clusters = single_link_clustering(matrix,100)
    colors = build_colors(clusters)
    plot_helper.plot(matrix,None, colors) 


def build_matrix_from_points(points):
    n = len(points)
    max = float('inf')
    matrix = []
    i = 0
    for i in range(0, n):
        row = []
        for j in range(0, n):
            
            u = points[i]
            v = points[j]
            
            row.append( (u[0]-v[0])**2 + (u[1]-v[1])**2 )
        
        matrix.append(row)
    
    return matrix

def test():
    points = [ (1,1), (1,4), (5,2), (6,2), (5,5), (6,5), (4,4), (7,5), (6,4), (10,10), (8,10),(3,4),(2,3) ]
    points = []
    n = 50
    for i in range(0,n):
        points.append( (randint(0,n),randint(0,n)) )
    #points = [ (1,1), (2,2) ]
    matrix = build_matrix_from_points(points)
    
    labels = range(0,len(matrix))
    clusters = single_link_clustering(matrix,10)
    plot_helper.plot_euclidean_points(points,None, build_colors(clusters))
    #plot_helper.plot(matrix,None, build_colors(single_link_clustering(matrix,4))) 
    
def testkmeans():
    max_tweets = 100
    data = read_twitter_data("../tweets.csv",max_tweets) #threshold on maximum tweets, > 500 gets slower due to there is a lot of words.
                                                 #That should be improved somehow in order to visualize data in a better way.
    print "finish reading data"
    adj =  build_distance(data)
    print "finish building distance"
    matrix,labels = build_adjacency_matrix(adj)
    k = 10

    clusters = k_means_clustering(matrix,k)
    colors = build_colors(clusters)
    plot_helper.plot(matrix,None, colors)     
    
    
#test_with_twitter_data()
testkmeans()
#test()
