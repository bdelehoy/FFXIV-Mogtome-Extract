from sys import argv
import urllib.request
from urllib.parse import urlparse
import csv

# External package imports
from bs4 import BeautifulSoup

# HTML tags and tag properties that uniquely define the data to look for
ITEM_LIST_IDENTIFIER    = {"class": "item__list__name"}
ITEM_COST_IDENTIFIER    = "td"

# Debug print flag
PRINT_ITEMS_FOUND       = False

def sanitize_url(s):
    parts = urlparse(s)
    assert parts.netloc.endswith("finalfantasyxiv.com")
    return s

def sanitize_csv_file_name(s):
    assert len(s) > 4
    if s[-4:] != ".csv":
        raise Exception("Filename must end in '.csv'")
    return s

################################

print(">> Initializing....")

url                     = sanitize_url(argv[1])
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

items = soup.find_all(attrs=ITEM_LIST_IDENTIFIER)
costs = soup.find_all(ITEM_COST_IDENTIFIER)
assert len(items) == len(costs)

result = []
for i,c in zip(items, costs):
    result.append((i.text, c.text))
    if PRINT_ITEMS_FOUND:
        print(i.text, c.text)

print()
print(">> Got", len(result), "items")

print(">> Writing to", output_filename)
if len(result) > 0:
    with open(output_filename, "w+", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([url])
        csv_writer.writerow([title])
        csv_writer.writerow([info])
        for i in result:
            csv_writer.writerow(i)
    print(">> Done!")
else:
    print(">> CSV failed to write (parsed no data)")
