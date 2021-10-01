import requests
import json

username = 'GBAleksandrGB'
token = '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'
repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
print(repos.status_code)
data = repos.json()
for repo in data:
    print(repo['html_url'])

with open('repo.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)
