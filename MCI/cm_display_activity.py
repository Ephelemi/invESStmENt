# Script to process usage data from the CommunityMirrorNetwork
# The script uses the Python ElasticSearch client library to access one index (one day)
# It retrieves DATA_TYPE and DATA_ID - and counts how often a particular DATA_ID
# apprears - The DATA_IDs then are mapped to titles using Personen-Export and
# Contents-Export from the CommunityMirror CMS

from elasticsearch import Elasticsearch
import csv
import datetime
import pandas as pd

# References:
# Python Client - see https://elasticsearch-py.readthedocs.io/en/v8.7.1/
# Using EQL - see https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html

# Instantiate a client instance
client = Elasticsearch("http://elk.informatik.unibw-muenchen.de:80")

print("Instantiated Elastic Search client instance - now doing query")

year='2023'
month='03'
day='23'

# Initialize the person list (map)
activity_list = []

# Init scroll by search
result_size = 0
data = client.search(
   index = 'usage-' + year + '.' + month + '.' + day,
   query = {"bool": { "should": [
         { "match": { 'ACTIVITY': 'TOUCHPRESSED' } },
         { "match": { 'ACTIVITY': 'TOUCHRELEASED' } },
         { "match": { 'ACTIVITY': 'DRAGGED' } },
         { "match": { 'ACTIVITY': 'TOUCH_RESHUFFLE_TEASER' } },
         { "match": { 'ACTIVITY': 'TOUCH_NEXT_VISUAL_STATE_DETAIL' } },
         { "match": { 'ACTIVITY': 'TOUCH_GRAPH_OPENED' } },
         { "match": { 'ACTIVITY': 'TOUCH_NEXT_VISUAL_STATE_PREVIEW' } },
         { "match": { 'ACTIVITY': 'TOUCH_GRAPH_CLOSED' } },
         { "match": { 'ACTIVITY': 'TOUCH_GRAPH_NAVIGATED' } },
         { "match": { 'ACTIVITY': 'TOUCH_SHOW_MESSHALLPLAN' } },
         { "match": { 'ACTIVITY': 'TOUCH_RESHUFFLE_FLOW' } },
         { "match": { 'ACTIVITY': 'TOUCH_CREATE_FLOW_ITEM' } },
         { "match": { 'ACTIVITY': 'TOUCH_SHOW_WEBVIEW' } },
         { "match": { 'ACTIVITY': 'User Touch' } },
         { "match": { 'ACTIVITY': 'GRAPH_CLOSED' } },
         { "match": { 'ACTIVITY': 'GRAPH_OPENED' } },
      ] } },

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
       timestamp = hit["_source"]['@timestamp']
       activity_list.append(timestamp)
    # Update the scroll ID
    data = client.scroll(scroll_id=sid, scroll='2m')
    sid = data['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])
    result_size += scroll_size
    print("returned %d hits" % scroll_size)

client.clear_scroll(scroll_id=sid)

print("\nGot %d hits altogether" % result_size)

with open('activities-' + year + '-' + month + '-' + day + '.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for activity in activity_list:
      spamwriter.writerow([activity])

print(type(datetime.datetime.now()))