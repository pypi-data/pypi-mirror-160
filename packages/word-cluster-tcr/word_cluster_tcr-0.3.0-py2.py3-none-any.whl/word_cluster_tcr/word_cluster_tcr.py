from itertools import combinations, groupby, product
from operator import itemgetter
import random
from typing import Counter

def hash_sort(words):
    data = Counter(words)
    data = list(data.keys())
    N = len(data)

    def tokenize(sequence):
        tokens = set()   
        for skip in range(len(sequence)):
            token = tuple(sequence[i] for i in range(len(sequence)) if i != skip)
            tokens.add(token)
        return tokens


    hashed_tokens = [(hash(t), i) for i in range(N) for t in tokenize(data[i])]
    hashed_tokens.sort(key=itemgetter(0))

    hash_clusters = []
    for h, g in groupby(hashed_tokens, key=itemgetter(0)):
        grouped_hashes = list(map(itemgetter(1), g))
        if len(grouped_hashes) != 1:
            hash_clusters.append(grouped_hashes)

    valid_clusters = []
    for cluster in hash_clusters:

        seq_tokens = [list(map(hash, combinations(data[seq_i], len(data[seq_i]) - 1))) for seq_i in cluster]

        valid = set()
        for s1, s2 in combinations(range(len(seq_tokens)), 2):
            t1 = seq_tokens[s1]
            t2 = seq_tokens[s2]
            if any(t1[i] == t2[i] for i in range(len(t1))):
                valid.add(cluster[s1])
                valid.add(cluster[s2])
        if valid:
            valid_clusters.append(valid)


    return valid_clusters