from collections import Counter

import numpy as np
from scipy import sparse
from sknetwork.clustering import Louvain


def group_clusters(vectors):
    grouped = {i: vectors[vectors == i].sum() for i in np.unique(vectors)}
    c = Counter(grouped)
    return c


def train_louvain_cluster(adj):

    # adj = edgelist2adjacency(edges)
    louvain = Louvain()
    clusters = louvain.fit_transform(sparse.csr_matrix(adj))
    return clusters
