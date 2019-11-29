
from nltk import ngrams
import re


from functools import reduce

def main():
    pass

def jaccard_coef(list1, list2,k1,k2):
    return list(map(lambda x: len(set(ngrams(list1,x)).intersection(set(ngrams(list2,x))))/len(set(ngrams(list1,x)).union(set(ngrams(list2,x)))),range(k1,k2+1)))

if __name__ == '__main__':
    main()