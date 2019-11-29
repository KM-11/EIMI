
from nltk import ngrams
import re
import os
from helper import load_env_file
from functools import reduce

def main():
    pass

def jaccard_coef(list1, list2,k1,k2):
    return list(map(lambda x: len(set(ngrams(list1,x)).intersection(set(ngrams(list2,x))))/len(set(ngrams(list1,x)).union(set(ngrams(list2,x)))),range(k1,k2+1)))


def look_write_files(syscall_traza):
    load_env_file()
    suspects_file = open(os.getenv('SUSPECT_FILES_PATH'),"r")
    detects=[]
    for tup in suspects_file.readlines():
        try:
            detects.append( tup.rstrip().split(",")[0],tup.rstrip().split(",")[1])
        except IndexError:
            print("Error de formato")
    resultcount=[]
    counter=0
    for i in detects:
        for ssys in syscall_traza:
            if(i[0]==ssys["syscall"]):
                for param in ssys["params"]:
                    if(i[1] in param):
                        counter=counter+1
        resultcount.append({i[0]:counter})
        counter=0






if __name__ == '__main__':
    main()