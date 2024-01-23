import argparse
import csv
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

################################

parser = argparse.ArgumentParser(
    description="Downloads Irregular Tomestone event rewards and writes them to a CSV file."
)
parser.add_argument(
    "-u",
    "--url",
    type=str,
    required=True,
    help="URL to a 'mogmog-collection' page on the FFXIV Lodestone.",
)
parser.add_argument(
    "-o",
    "--output-file",
    type=str,
    default="output.csv",
    help="CSV file in this script's directory to write results to. Will be created if it doesn't exist.",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="If provided, prints out parsed text from the webpage to the console.",
)

################################


def sanitize_url(s) -> tuple[str, datetime]:
    parts = urlparse(s)
    if not parts.netloc.endswith("finalfantasyxiv.com"):
        raise ValueError(
            f"URL must belong to the domain 'finalfantasyxiv.com'\nGot: '{parts.netloc}' (via {s})"
        )
    event_period_from_url = parts.path.split("/")[-2]
    yearmonth = datetime.strptime(event_period_from_url, "%Y%m")
    return (s, yearmonth)


def sanitize_csv_file_name(s) -> str:
    if len(s) > 4 and s[-4:] == ".csv":
        return s
    raise NameError(f"Output filename must end in '.csv'\nGot: '{s}'")


def get_cmd_line_inputs(inp: argparse.Namespace) -> tuple[str, datetime, bool, str]:
    url, yearmonth = sanitize_url(inp.url)
    output_filename = sanitize_csv_file_name(inp.output_file)
    verbose = inp.verbose
    return (url, yearmonth, output_filename, verbose)


def get_items_and_costs(
    s: BeautifulSoup, item_list_html_id: dict, cost_html_id: str
) -> list[tuple[str, int]]:
    items = s.find_all(attrs=item_list_html_id)
    costs = s.find_all(cost_html_id)
    assert len(items) == len(costs)

    result = []
    for i, c in zip(items, costs):
        result.append((i.text, int(c.text)))
    return result


def write_csv(output_filename: Path, data) -> None:
    if len(data) > 0:
        full_path = Path(".", output_filename).resolve()
        with open(full_path, "w+", encoding="utf-8", newline="") as csv_file:
            csv_writer = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            csv_writer.writerow([URL])
            csv_writer.writerow([title])
            csv_writer.writerow([info])
            csv_writer.writerow(["ITEM", "COST"])
            for i in data:
                csv_writer.writerow(i)
    return


################################

# HTML tags and tag properties that uniquely define web elements to look for
ITEM_LIST_IDENTIFIER = {"class": "item__list__name"}
ITEM_COST_IDENTIFIER = "td"

if __name__ == "__main__":
    # Sample URL: https://na.finalfantasyxiv.com/lodestone/special/mogmog-collection/202304/y7377p4z7j

    URL, EVENT_PERIOD, OUTPUT_FILENAME, VERBOSE = get_cmd_line_inputs(parser.parse_args())
    print(f"URL:            {URL}")
    print(f"Event period:   {EVENT_PERIOD.strftime('%b %Y')}")
    print(f"Output file:    {OUTPUT_FILENAME}")
    print(f"Verbose output: {VERBOSE}")
    print()
    print("Working....")

    with urllib.request.urlopen(URL) as handler:
        soup = BeautifulSoup(handler, "html.parser")

    title = soup.title.text
    info = soup.find_all("meta")[1]["content"]
    if VERBOSE:
        print()
        print(f"> {title}")
        print(f"> {info}")

    all_items = get_items_and_costs(soup, ITEM_LIST_IDENTIFIER, ITEM_COST_IDENTIFIER)
    if VERBOSE:
        print()
        for i, c in all_items:
            print(f"> {i} (Cost: {c})")

    print()
    print("Got", len(all_items), "items")

    print(f"Writing to {OUTPUT_FILENAME}")
    write_csv(OUTPUT_FILENAME, all_items)
    print("Done!")
