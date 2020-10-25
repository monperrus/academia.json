#!/usr/bin/python3
# checks that all DBLP code names are correct

import json
import requests

data = json.load(open('academia.json'))

for i,v in data.items():
  codes = v['dblp_code']
  if type(codes) == str: codes = [codes]
  
  for x in codes:
    dblp_data = requests.get('https://dblp.org/search/publ/api/?q=venue:'+x+'&format=json').json()['result']['hits']
    if 'hit' not in dblp_data or len(dblp_data['hit']) < 30:
      raise Exception(x)
    print(x,len(dblp_data['hit']))
