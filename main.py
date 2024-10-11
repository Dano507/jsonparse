from pprint import pprint
import jsonparse


# Swap FILE with different ones from samples/
# to verify that jsonparse works
FILE = "samples/3dim-both.json"

rawjsonstring = None
with open(FILE) as f:
    rawjsonstring = f.read()


parsed = jsonparse.parse(rawjsonstring)
pprint(parsed)
