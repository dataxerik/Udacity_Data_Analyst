#### Overview

The aim of this project is to take raw xml data for any location from mapzen, access the data and look for inconsistency, clean the data, and then, finally, add this data to a database. The data I choose was an extract of metro Tokyo, Japan, which can be found here. It contains about 4 GB of metro data.

#### Data Assessment

One of the biggest challenges of this data set is its size. This is really first attempt at working with unclean data of this size, so looking at this data for any kind issues is challenging.

#### Prerequisite

Since this class is taught in English, I wanted to cover some things that are unique to this dataset because it comes from another country.
##### Address

Since I'm dealing with address in Japan, what does a standard Japanese address look like? One interesting thing is that address goes from largest to smallest ie Zip Code, Prefecture, Ward, Block, Building Number, Name. If I were to use write a US address in this style it would be Zip Code, State, City, Street, Street Number, and Name. An example of an actuall Japanese address is below.

```
〒100-8994
東京都中央区八重洲一丁目5番3号
東京中央郵便局

or

〒100-8994
Tokyo Prefecture Central Ward Yaesu 1st District 5th block Building Number 3
Tokyo Central Post Office
```

One import note is that we can abbreviate 一丁目5番3号 to 1-5-3. So, we should expect various combinations of this format.

<table>
	<tr>
		<td>Word</td>
		<td>Meaning</td>
	</tr>
	<tr>
		<td>東京都</td>
		<td>Tokyo Prefecture</td>
	</tr>
	<tr>
		<td>中央区</td>
		<td>Central Ward</td>
	</tr>
	<tr>
		<td>八重洲一丁目</td>
		<td>Yaesu 1st District</td>
	</tr>
	<tr>
		<td>5番</td>
		<td>5th block</td>
	</tr>
	<tr>
		<td>3号</td>
		<td>Building Number 3</td>
	</tr>
	<tr>
		<td>東京中央郵便局</td>
		<td>Tokyo Central Post Office</td>
	</tr>
</table>

#### KSJ2

In a preview of ways to come, KSJ2 is data that comes from Ministery of Land, Infrastructure, and Transport(MLIT) of Japan.

KSJ2 collects information on various things such as Airports and Railways. And, data imported from KSJ2 have special tags who meaning isn't clear on first glance. So, here's an overview on various tags and their meanings.

<table>
    <tr>
        <td colspan='2'>Airport Code Meanings</td>
    <tr>
	<tr>
		<td>Abbreviation</td>
		<td>Meaning</td>
	</tr>
	<tr>
		<td>OPC</td>
		<td>Operational City</td>
	</tr>
	<tr>
		<td>LIN</td>
		<td>Railway Line Name</td>
	</tr>
	<tr>
		<td>RAC</td>
		<td>Railway Type</td>
	</tr>
	<tr>
		<td>INT</td>
		<td>Service Provider Type</td>
	</tr>
</table>

(reference)[http://wiki.openstreetmap.org/wiki/Talk:Import/Catalogue/Japan_KSJ2_Import]
OSM Data Structure

An .osm is a file with a XML strcuture. And, it contains five tags: nodes, ways, closed ways, areas, and relation. In this analysis, we are only looking at nodes and ways tags. Nodes tags are used to mark locations and may be separated or connected. Ways tags are connection lines between nodes. And, noth nodes and ways tags can have child tags, which are tags that contain key-value pairs. These key-value pairs describe the node or way. For example,

reference
Analysis

I took a fairly large extract, so I wanted to get a file for how many nodes and wat tages existed in this file. So, I looked for all the tag elements using the below code. Futhermore, To get a understanding on how long it would take to read the whole file, I timed this script as well.

```
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
    return i , j

start_time = time.time()
print(find_number_of_node_ways(file))
print(time.time() - start_time)

#Results
(38380190, 5990342)
497.622065782547
```

In other words, there are 38380190 nodes and 5990342 way tag elements. Now, since we are looking at 'start' and 'end', I need to divide the two number in halfs to get the total number of observations. Therefore, the total number of observations is 19190095 and 2995171. And, it takes about 8 minutes to read all the data.

So, to better assess what kind of data each node and way have. I looped through the file again looking for wag and node tags and their children and converted it into a dictionary then wrote dump the dictionary into a file. The function that I used is below.

```
def get_key_values(file_, limit=True, limit_num = 30000):
    i = 0
    tag_keys = {}
    tag_tag_keys = {}
    tag_addr = defaultdict(set)
    context = ET.iterparse(file_, events=('start', 'end'))
    _, root = next(context)

    for _, elem in context:
        if limit and i == limit_num:
            break

        if elem.tag == 'way':
            for att in elem.keys():
                for tag in elem.iter('tag'):
                    tag_key = tag.get('k')
                    if tag_tag_keys.get(tag_key) is None:
                        tag_tag_keys[tag_key] = 1
                    else:
                        tag_tag_keys[tag_key] += 1
                if tag_keys.get(att) is None:
                    tag_keys[att] = 1
                else:
                    tag_keys[att] += 1
        elem.clear()
        i += 1
    write_dic_to_file(tag_keys, 'way_key.txt')
    write_dic_to_file(tag_tag_keys, 'way_tag_keys.txt')
```

#### Node Assessment

The number of attributes match the number of nodes we have, so we have a complete set.

{
    "changeset": 19190095,
    "id": 19190095,
    "lat": 19190095,
    "lon": 19190095,
    "timestamp": 19190095,
    "uid": 19190095,
    "user": 19190095,
    "version": 19190095
}

There are many different kind of node tags, so I wouldn't provied the full list in this document, but it will be include as supplemented material. However, I will note down abnormalities I see.

#### Fix me!

One thing that immediatedly caught my eye was the 'FIXME', 'FIXME:ja', and 'Fixme' tags. There are total of 1921 fixme tags. it seems there might be some issues with certain nodes besides consistency. The could be someone wrong with the data itself. For example, a frequent request from the fixme tag is to fix the bus stop position. 'このバス停を正しい位置に移動させて欲しい' (Please move the bus stop to the correct position) with 965 and このバス停を正しい位置に移動させて欲しい with 332. In total, 1297 fixme tags out of 1921 related to bus stop position. So, I boarded my search by using this regex 'バス停.+位置', which means 'bus stop.+position' and got a count of 1352. So, about 70% of the fixme tags related to bus stop position.

```
{
    "changeset": 2995171,
    "id": 2995171,
    "timestamp": 2995171,
    "uid": 2995171,
    "user": 2995171,
    "version": 2995171
}
```
