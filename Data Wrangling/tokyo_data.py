import xml.etree.cElementTree as ET
import time
import re
from collections import defaultdict
file = 'C:\\Users\\dsharp\\Downloads\\tokyo_japan.osm\\tokyo_japan.osm'
#file = 'C:\\Users\\dsharp\\PycharmProjects\\Udacity\\text.txt'


def sample_file(file_, context_):
    with open(file_, 'w') as fout:
        i = 0
        for _, elem in context_:

            if i == 100000:
                break
            print(i)
            fout.write(str(ET.tostring(elem)))
            elem.clear()
            i += 1

start_time = time.time()
context = ET.iterparse(file, events=('start', 'end'))

i = 0

_, root = next(context)

tag_keys = {}
tag_tag_keys = {}
tag_addr = defaultdict(set)

for _, elem in context:
    '''
    if i == 300000:
        break
    '''
    if elem.tag == 'node':
        for att in elem.keys():
            for tag in elem.iter('tag'):
                tag_key = tag.get('k')
                #print(ET.tostring(tag))
                #print(tag.get('k'), tag.get('v'))
                #print(tag.get('v'))
                '''
                if tag_key == 'religion':
                    print(tag.get('v'))
                '''
                if tag_tag_keys.get(tag_key) is None:
                    tag_tag_keys[tag_key] = 1
                else:
                    tag_tag_keys[tag_key] += 1

                if re.search('^addr+', tag_key):
                    print(tag.get('v'))
                    tag_addr[tag_key].add(tag.get('v'))
            if tag_keys.get(att) is None:
                tag_keys[att] = 1
            else:
                tag_keys[att] += 1
    elem.clear()
    i += 1

print(tag_keys)
print(tag_tag_keys)
print(i)
print(tag_addr)
print(time.time() - start_time)
