import xml.etree.cElementTree as ET
import time
import json
import re
from collections import defaultdict

file = 'C:\\Users\\dsharp\\Downloads\\tokyo_japan.osm\\tokyo_japan.osm'


# file = 'C:\\Users\\dsharp\\PycharmProjects\\Udacity\\text.txt'
# print(ET.tostring(tag))

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


def write_dic_to_file(dic_, file_):
    with open(file_, 'w') as fin:
        fin.write(json.dumps(dic_, sort_keys=True, indent=4))


def get_key_values(file_, limit=True, limit_num=30000):
    i = 0
    tag_keys = {}
    tag_tag_keys = {}
    context = ET.iterparse(file_, events=('start', 'end'))
    _, root = next(context)

    for _, elem in context:
        if limit and i == limit_num:
            break

        if elem.tag == 'node':
            for tag in elem.iter('tag'):
                tag_key = tag.get('k')
                if tag_key is None:
                    break
                if tag_tag_keys.get(tag_key) is None:
                    tag_tag_keys[tag_key] = 1
                else:
                    tag_tag_keys[tag_key] += 1
                '''
                if re.search('^addr+', tag_key):
                    tag_addr[tag_key].add(tag.get('v'))
                '''
        elem.clear()
        i += 1
    print(tag_tag_keys)
    print(tag_tag_keys.items())
    # write_dic_to_file(tag_keys, 'node_key.txt')
    write_dic_to_file(tag_tag_keys, 'node_tag_keys1.txt')
    return tag_keys, tag_tag_keys


def find_number_of_node_ways(file_):
    i, j = 0, 0
    context = ET.iterparse(file_, events=('start', 'end'))
    _, root = next(context)
    for _, elem in context:
        if elem.tag == 'node':
            i += 1
        elif elem.tag == 'way':
            j += 1
        elem.clear()
    return i, j


def find_tag_attribute(file_, tag_name, target_file, limit=True, limit_num=50000):
    i = 0
    tag_addr = defaultdict(int)
    context = ET.iterparse(file_, events=('start', 'end'))
    _, root = next(context)

    for _, elem in context:
        if limit and i == limit_num:
            break

        if elem.tag == 'node':
            for tag in elem.iter('tag'):
                tag_value = tag.get('v')
                tag_key = tag.get('k')
                if tag_key is not None and re.search(tag_name, tag.get('k'), re.I):
                    tag_addr[tag_value] += 1
        elem.clear()
        i += 1
    write_dic_to_file(tag_addr, target_file)
    print(tag_addr)


def read_file(file_):
    temp = {}
    with open(file_) as fout:
        temp = json.load(fout)
    return temp


def check_regex(dict_, word_):
    temp = []
    for key in dict_.keys():
        if re.search(word_, key, re.I):
            temp.append(key)
    return temp


def get_value_count(dict_, word_):
    count = 0
    for key in dict_.keys():
        if re.search(word_, key, re.I):
            count += dict_[key]
    return count


def find_kanji_chome_tags(dict_):
    #'丁目[1-9]+－.?'
    block_pattern = re.compile('丁目.?－[0-9]', re.U)
    space_pattern = re.compile('－', re.U)
    print(u'\xFF01', u'\xFF0E')
    for key in dict_.keys():
        #print(key)
        if block_pattern.match(key):
            print(key)
            #if space_pattern.search(key):
            #    print(key)


start_time = time.time()
# print(find_number_of_node_ways(file))
# print(get_key_values(file, limit=False))
# tag_list = read_file('node_tag_keys.txt')
# print(len(tag_list))
# find_tag_attribute(file, '^addr$', 'addr_values.txt', False)
# temp = read_file('node_tag_keys.txt')
# print(check_regex(temp, '^addr$'))
temp = read_file('addr_values.txt')
find_kanji_chome_tags(temp)
# print(get_value_count(temp, 'バス停.+位置'))
# print(sorted(temp.items(), key=lambda x: -x[1]))
# print(sum(temp.values()))
print(time.time() - start_time)
