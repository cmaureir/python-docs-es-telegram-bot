import re
import requests
from bs4 import BeautifulSoup

from lib.common import clean

def get_progress_data():
    purl = "https://python-docs-es.readthedocs.io/es/3.8/progress.html"
    r = requests.get(purl)
    if r.status_code != 200:
        return None

    page = r.text
    if not page:
        return None

    data = {}
    soup = BeautifulSoup(page, features="html.parser")
    # Get the first <pre> section
    div = soup.findAll("pre")[0]
    lines = [i for i in div.text.split("\n") if i]

    # Regular expressions
    re_percentage = re.compile(r"(\d+(?:\.\d+)?)%")
    re_title = re.compile(r"# (.*) \(")
    re_filename = re.compile(r"- (.*)\.po")
    re_entries = re.compile(r" (\d+\s{1,}/\s{1,}\d+) \(")

    for line in lines:
        percentage = 0
        if percentage_search := re_percentage.search(line):
            percentage = percentage_search.group(1)

        if line.startswith("#"):
            title = ""
            if title_search := re_title.search(line):
                title = title_search.group(1).strip()
            if not title:
                title = "misc"
            if title not in data:
                data[title] = {"percentage": percentage}

        elif line.startswith("-"):
            filename = ""
            entries = ""
            if filename_search := re_filename.search(line):
                filename = filename_search.group(1).strip()
            if entries_search := re_entries.search(line):
                entries = entries_search.group(1).strip()

            if filename not in data[title]:
                data[title][filename] = {"entries": entries,
                                         "percentage": percentage}

    # Completed files
    div = soup.findAll("pre")[1]
    lines = [i for i in div.text.split("\n") if i]
    data["Completados"] = {"percentage": len(lines) - 1}
    return data




# /progress
def get_progress():
    data = get_progress_data()
    if not data:
        return None
    length = max(len(i) for i in data.keys()) + 1
    message = ''.join(f"{key:<{length}}: ({value['percentage']:>5}%)\n"
                      for key, value in data.items() if key != "Completados")

    msg = f"*Progress*\n```\n{clean(message)}\n```"
    msg += f"\nArchivos completados: {data['Completados']['percentage']}"
    return msg


# /progress <TITLE>
def get_progress_details(title):
    data = get_progress_data()
    if title not in data:
        return f"Section: *{clean(title)}* not found"

    length = max(len(i) for i in data[title].keys()) + 3
    message = ''.join(f"{key:<{length}}: {value['entries']:>9} ({value['percentage']:>5}%)\n"
                      for key, value in data[title].items() if key != "percentage")
    return f"Section *{clean(title)}* {clean(data[title]['percentage'])}%\n```\n{clean(message)}\n```"
