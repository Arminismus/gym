import dill
from collections import defaultdict
q_table = defaultdict(lambda:0)

def save(table,name):
    with open(name,'wb') as fp:
        dill.dump(table,fp)

def load(name):
    with open(name,'rb') as fp:
        return dill.load(fp)
