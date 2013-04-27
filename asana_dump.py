import os
import sys
import time
import json
import requests

ADDR = "https://app.asana.com/api/1.0"

if 'ASANA_KEY' not in os.environ:
  raise RuntimeError("Please define your Asana API key in the 'ASANA_KEY' environment variable.")
KEY = os.environ['ASANA_KEY']

def get(path, raw=False, **params):
  res = requests.get("%s/%s" % (ADDR, path), auth=(KEY, ""), params=params)
  return res.text if raw else res.json()
  
usage = "USAGE: asana_dump.py [project_id]"
  
if __name__ == "__main__":

  if len(sys.argv) == 2:
    
    out = sys.stdout
    tasks = get("projects/%s/tasks" % sys.argv[1])['data']
    for task in tasks:
      task_data = get("tasks/%s" % task['id'])
      stories = get("tasks/%s/stories" % task['id'])['data']
      task_data['stories'] = stories
      json.dump(task_data, out, indent=True)
      time.sleep(0.1)
    
  elif len(sys.argv) == 1:

    print usage
    print ""
    print "Projects available:"
    print "====================="
    data = get("users/me")['data']
    for ws in data['workspaces']: 
      print "In workspace '%s'" % ws['name']
      print "------------"
      projects = get("workspaces/%s/projects" % ws['id'])['data']
      for p in projects:
        print "%s:\t%s" % (p['id'], p['name'])
