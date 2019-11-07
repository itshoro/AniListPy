import requests, json

class GqlClient:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def request(self, query, variables = None):
        body = { "query": query, "variables": variables }
        response = requests.post(self.url, headers=self.headers, json=body)

        if response.status_code >= 400:
            raise TypeError(f"Request produced a {response.status_code} - {response.reason}\n" + response.text)

        return response