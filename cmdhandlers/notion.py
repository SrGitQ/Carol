import requests, json
from licenses import getSchDB, getNotionHeaders

def getNotionDatabase():
    readUrl = f"https://api.notion.com/v1/databases/{getSchDB()}/query"

    res = requests.post(readUrl, headers=getNotionHeaders())
    data = res.json()
    return data['results']
