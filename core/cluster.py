from helper import *
from nltk import ngrams

UMBRAL = 60
NGRAM = 8


def get_ngram(opcodes_func, ngram):
    n_grams = []
    for func in opcodes_func:
        n_grams.extend(list(ngrams(opcodes_func[func], ngram)))

    return n_grams


def inserta_cluster(hash, type, id):
    pass


def cluster_ngrams(sample):
    muestras = get_data_bbdd('static_anal', sample.md5, 'web_familia', 'n_grams')
    best = ''
    best_score = 0

    for muestra in muestras:
        index = jaccard_index(get_ngram(sample.opcodes_func, NGRAM), get_ngram(muestra['opcodes_func'], NGRAM))

        if index > best_score:
            best_score = index
            best = muestra['name']
        if index > UMBRAL:
            print(colored("[+] " + muestra['name'] + ": " + str(index) + "%", 'green'))
        # if best_score > UMBRAL:
        # INSERT MISMO CLUSTER best


def cluster_cc(sample):
    muestras = get_data_bbdd('static_anal', sample.md5, 'web_familia', 'cc')
    best = ''
    best_score = 0
    for muestra in muestras:
        index = structural_similarity(sample.cc, muestra['cc'])
        if index >= best_score:
            best_score = index
            best = muestra['name']
        if index > UMBRAL:
            print(colored("[+] " + muestra['name'] + ": " + str(index) + "%", 'green'))
        # if best_score > UMBRAL:
        # INSERT MISMO CLUSTER best


# if best_score > UMBRAL:
# INSERT MISMO CLUSTER CC best

def cluster_dinamico(sample):
    muestras = get_data_bbdd('static_anal', sample.md5, 'web_familia', 'dinamico')
