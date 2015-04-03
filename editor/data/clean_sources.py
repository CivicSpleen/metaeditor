# Load the sources, organize them by parent it, and output a revision. 
import csv
from collections import defaultdict

fn_in = 'sources.csv'
fn_out = "sources-revised.csv"

class Source:
   
    def __init__(self):
        self.id = None
        self.name = None
        self.parent_id = None
        self.children = set()

sources = defaultdict(Source)

with open(fn_in) as f:
    header = csv.reader(f).next()
    
with open(fn_in) as f:
    r = csv.DictReader(f)
    for row in r:
       
        source = sources[int(row['id'])]
        for k,v in row.items():
            setattr(source, k, v)
        
        try:
            parent = sources[int(row['parent_id'])]
            parent.children.add(source.id)
        except ValueError:
            pass
            


def dump(sources, w, id_):
    id_ = int(id_)
    d = dict(sources[id_].__dict__.items())

    del d['children']
    w.writerow(d)
    
    for child in sources[id_].children:
        dump(sources, w, child)


with open(fn_out, 'w') as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    dump(sources, w, 1)

