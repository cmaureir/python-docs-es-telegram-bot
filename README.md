# Python Docs Es Bot

Telegram Bot for the [python-docs-es](https://github.com/python/python-docs-es)
group, which is behind the effort of translating the official Python
documentation to Spanish.

## Usage

* `/progress` to get a general summary of the Translation progress.
* `/progress <section>` to get details of the specific 'section'.
  (e.g.: `/progress c-api`)

* `/prs` to get a list of all the open Pull-requests
* `/prs <ID>` get details of the specific Pull-request 'ID'
  (e.g.: `/prs 292`)

## Data source

* The `/progress` command query the website: https://python-docs-es.readthedocs.io/es/3.8/progress.html
* The `/prs` command query the PRs from the repository: https://github.com/python/python-docs-es/pulls
