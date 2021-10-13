# Python 3.9.7

# Sample command (Oct-Nov 2021 Pre-Endwalker Moogle Tome event):
# python mogtome-extract.py https://na.finalfantasyxiv.com/lodestone/special/mogmog-collection/202110/7pBwXOpUFp output.csv

# External package imports (virtual environment is recommended)
from bs4 import BeautifulSoup

from sys import argv
import urllib.request
import csv

def sanitize_csv_file_name(s):
    assert len(s) > 4
    if s[-4:] != ".csv":
        raise Exception("Filename must end in '.csv'")
    return s

url                     = argv[1]
output_filename         = sanitize_csv_file_name(argv[2])

fp = urllib.request.urlopen(url)
soup = BeautifulSoup(fp, "html.parser")
fp.close()

title = soup.title.text
print(title)

info = ""
try:
    info = soup.find_all('meta')[1]['content']
    print(info)
except:
    print(">> Could not fetch event description")

print()

ITEM_LIST_IDENTIFIER    = {"class": "item__list__name"}
ITEM_COST_IDENTIFIER    = "td"

items = soup.find_all(attrs=ITEM_LIST_IDENTIFIER)
costs = soup.find_all(ITEM_COST_IDENTIFIER)
assert len(items) == len(costs)

result = []
for i,c in zip(items, costs):
    result.append((i.text, c.text))
    print(i.text, c.text)

print()
print(">> Got", len(result), "items")

if len(result) > 0:
    with open(output_filename, "w+", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([url])
        csv_writer.writerow([title])
        csv_writer.writerow([info])
        for i in result:
            csv_writer.writerow(i)
    print(">> Wrote to " + output_filename)
else:
    print(">> CSV not written (empty results)")

print(">> Done!")
