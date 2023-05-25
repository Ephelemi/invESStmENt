# Script to process usage data from the CommunityMirrorNetwork
# The script uses the Python ElasticSearch client library to access one index (one day)
# It retrieves DATA_TYPE and DATA_ID - and counts how often a particular DATA_ID
# apprears - The DATA_IDs then are mapped to titles using Personen-Export and
# Contents-Export from the CommunityMirror CMS

from elasticsearch import Elasticsearch
import csv
import datetime

# References:
# Python Client - see https://elasticsearch-py.readthedocs.io/en/v8.7.1/
# Using EQL - see https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html

# Load DATA_ID - Title data from files exported from the Wordpress CMS
cms_content_list = {}
with open('Personen-Export.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        cms_content_list[row[0]] = row[1]
with open('Contents-Export.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        cms_content_list[row[0]] = row[1]

# Instantiate a client instance
client = Elasticsearch("http://elk.informatik.unibw-muenchen.de:80")

print("Instantiated Elastic Search client instance - now doing query")

# Initialize the person list (map)
person_list = {}

# Init scroll by search
result_size = 0
data = client.search(
   index = 'usage-2023.04.26',
   query = {"bool": { "must": [ { "match": { 'TYPE': 'DISPLAY_SHOW' } }, {  "match": { 'DATA_TYPE': 'person' } } ] } },
   scroll = '2m', # length of time to keep search context
   size = 10000
)

# Get the scroll ID
sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])
result_size += scroll_size
print("returned %d hits" % scroll_size)

# Retrieve next page of results
while scroll_size > 0:
    # Iterate through batch of results
    for hit in data['hits']['hits']:
       data_type = hit["_source"]['DATA_TYPE']
       data_id = hit["_source"]['DATA_ID']
       if data_id in person_list:
          person_list[data_id] += 1
       else:
          person_list[data_id] = 1
    # Update the scroll ID
    data = client.scroll(scroll_id=sid, scroll='2m')
    sid = data['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])
    result_size += scroll_size
    print("returned %d hits" % scroll_size)
    
client.clear_scroll(scroll_id=sid)

print("Got %d hits altogether" % result_size)

# Now print results
for data_id, score in person_list.items():
   label = data_id
   if (label.startswith('wp://cms.communitymirrors.net:')):
     label = cms_content_list[label[30:]];
   print(label + ": " + str(score))