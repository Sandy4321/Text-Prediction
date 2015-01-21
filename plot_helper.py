from __future__ import division
 
import numpy as np
import matplotlib.pyplot as plt
import random

def cmdscale(D):
    """                                                                                       
    Classical multidimensional scaling (MDS)                                                  
                                                                                               
    Parameters                                                                                
    ----------                                                                                
    D : (n, n) array                                                                          
        Symmetric distance matrix.                                                            
                                                                                               
    Returns                                                                                   
    -------                                                                                   
    Y : (n, p) array                                                                          
        Configuration matrix. Each column represents a dimension. Only the                    
        p dimensions corresponding to positive eigenvalues of B are returned.                 
        Note that each dimension is only determined up to an overall sign,                    
        corresponding to a reflection.                                                        
                                                                                               
    e : (n,) array                                                                            
        Eigenvalues of B.                                                                     
                                                                                               
    """
    # Number of points                                                                        
    n = len(D)
 
    # Centering matrix                                                                        
    H = np.eye(n) - np.ones((n, n))/n
 
    # YY^T                                                                                    
    B = -H.dot(np.power(D,2)).dot(H)/2
 
    # Diagonalize                                                                             
    evals, evecs = np.linalg.eigh(B)
 
    # Sort by eigenvalue in descending order                                                  
    idx   = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:,idx]
 
    # Compute the coordinates using positive-eigenvalued components only                      
    w, = np.where(evals > 0)
    L  = np.diag(np.sqrt(evals[w]))
    V  = evecs[:,w]
    Y  = V.dot(L)
 
    return Y, evals

def to_x_y(data):
    mds = cmdscale(data)
    x = []
    y = []
    for t in mds[0]:
        x.append(t[1])
        y.append(t[0])
    return x,y
    

def plot(data,labels,clusters):
    mds = cmdscale(data)
    x = []
    y = []
    for t in mds[0]:
        x.append(t[1])
        y.append(t[0])
    
    
    fig, ax = plt.subplots()
    #colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in clusters])
    plt.scatter(x,y,c=clusters,s=100)
    
    if labels != None:
        for i,label in enumerate(labels):
            ax.annotate(label,(x[i],y[i]))
    
        
    
    plt.ylabel('some numbers')
    plt.show()

def plot_euclidean_points(data,labels,clusters):
    x = []
    y = []
    for t in data:
        x.append(t[0])
        y.append(t[1])
    
    print x,y
    
    fig, ax = plt.subplots()
    #colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in clusters])
    plt.scatter(x,y,c=clusters,s=100)
    
    if labels != None:
        for i,label in enumerate(labels):
            ax.annotate(label,(x[i],y[i]))
    
        
    
    plt.ylabel('some numbers')
    plt.show()
    
def random_data(n):
    maxm = n
    m = n*[[maxm]*n]
    for u in range(0,n):
        for v in range(0,n):
            if u == v:
                m[u][v] = 0
            else:
                m[u][v] = random.randint(0,maxm)
                m[v][u] = random.randint(0,maxm)

    return m
    
