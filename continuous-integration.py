#!/usr/bin/python3
# checks that all fields are correct
# runs monthly on Travis

import json
import requests
import time
import random

data = json.load(open('academia.json'))
random.shuffle(data)

ndblp = 0
for v in data:
  codes = v['dblp_code']
  if type(codes) == str: codes = [codes]
  
  # find issn for journals
  # # if "long_name" not in v: raise Exception()
  # if "long_name" in v and v["long_name"] != "":
  #   resp_crossref = requests.get("https://api.crossref.org/works?query.container-title="+v["long_name"])
  #   for x in resp_crossref.json()["message"]["items"]:
  #     #del x["references"]
  #     if "issn-type" in x:
  #       # sometimes we have two
  #       v["issn"] = x["issn-type"][0]["value"]
  #       print(v["long_name"], x["issn-type"][0]["value"])
  #   continue

  # find long names for conference OK
  # find issn for conference KO -> not in the crossref output
  # this does not work in DBLP API not a long name
  # if v["type"] == "conference":
  #   resp = requests.get('https://dblp.org/search/publ/api/?q=venue:'+codes[-1]+':&format=json').json()
  #   # api is rate limitaed but I don't know how, 
  #   # .5 is not enough
  #   time.sleep(.8)
  #   if len(resp['result']['hits']['hit'])>0:
  #     paper = resp['result']['hits']['hit'][0]
  #     print(codes, "https://doi.org/"+paper["info"]["doi"])
  #     # ['ASE'] {'@score': '1', '@id': '772328', 'info': {'authors': {'author': [{'@pid': '205/8755', 'text': 'Tooba Aamir'}, {'@pid': '48/6411', 'text': 'Mohan Baruwal Chhetri'}, {'@pid': '173/5818', 'text': 'M. A. P. Chamikara'}, {'@pid': '00/10437', 'text': 'Marthie Grobler'}]}, 'title': 'Government Mobile Apps: Analysing Citizen Feedback via App Reviews.', 'venue': 'ASE', 'pages': '1858-1863', 'year': '2023', 'type': 'Conference and Workshop Papers', 'access': 'closed', 'key': 'conf/kbse/AamirCCG23', 'doi': '10.1109/ASE56229.2023.00190', 'ee': 'https://doi.org/10.1109/ASE56229.2023.00190', 'url': 'https://dblp.org/rec/conf/kbse/AamirCCG23'}, 'url': 'URL#772328'}
  #     resp_crossref = requests.get("https://api.crossref.org/works?filter=doi:"+paper["info"]["doi"]).json()
  #     # print(resp_crossref.json()["message"]["items"][0])
  #     # no issn here but a long name
  #     if len(resp_crossref["message"]["items"]) > 0:
  #       print(resp_crossref["message"]["items"][0]["container-title"][0])
    
# with open("academia.json", "w") as f: json.dump(data, f, indent=2)
# if False:  

  # check is RSS is not 404
  # sciencedirect 403 from python, grrrrrr
  # ieee xplore returns 418 I'm a teapot
  if "rss" in v \
    and "sciencedirect" not in  v["rss"] \
    and "ieeexplore.ieee.org" not in  v["rss"] \
    :
    resp_rss = requests.get(v["rss"], headers = {"user-agent":"Mozilla/5.0"})
    if resp_rss.status_code != 200:
      raise Exception("rss not correct "+ str(resp_rss.status_code)+ " "+ str(v))
    print(v["rss"], "ok HTTP 200")

  sample_codes = random.sample(codes, min(2, len(codes)))
  for x in sample_codes:
    try:
      if ndblp > 5:
        print("reached 100, stopping to avoid hitting rate limit")
        break
      url = 'https://dblp.org/search/publ/api/?q=venue:'+x+':&format=json'
      print("checking dblp code", url)
      resp = requests.get(url)
      ndblp += 1
      # api is rate limited but I don't know how, 
      # .5 is not enough
      time.sleep(2)
      if resp.status_code != 200:
        print(resp.status_code)
        print(resp.headers)
        # there is some rate limit
        print(resp.text) # The user has sent too many requests in a given amount of time.
        
      dblp_data = resp.json()['result']['hits']
      if 'hit' not in dblp_data or len(dblp_data['hit']) < 30:
        raise Exception(x)
      print(x,len(dblp_data['hit']))
    except Exception as e:
      print("error for",x)
      raise e
