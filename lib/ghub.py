import requests

from lib.common import clean

def get_prs_data():
    gurl = "https://api.github.com/repos/python/python-docs-es/pulls"
    params = dict(state="open")
    r = requests.get(url=gurl, params=params)
    if r.status_code != 200:
        print("WARNING: Empty request")
        return None
    return r.json()

# /prs
def get_prs():
    prs = get_prs_data()
    message = ''.join(f" \- [{pr['number']}](https://github.com/python/python-docs-es/pull/{pr['number']}) {clean(pr['title'].strip())}\n" for pr in prs)
    return f"*Open PRs*\n{message}"


# /prs <ID>
def get_prs_details(pr_id):
    prs = get_prs_data()
    for pr in prs:
        if pr["number"] == pr_id:
            details = f"[{pr['user']['login']}](https://github.com/{pr['user']['login']})\n".replace("-", "\-")
            message = (f"\#{pr['number']} *{clean(pr['title'])}* by "
                       f"{details}"
                       f"Last update: {clean(pr['updated_at'])}\n"
                       f"{clean(pr['html_url'])}\n")
            return message
    return f"PR *\#{pr_id}* not found"

