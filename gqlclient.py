import requests, json

class GqlClient:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def request(self, query, variables = None, method = "POST"):
        body = { "query": query, "variables": variables }

        if method == "POST":
            response = requests.post(self.url, headers=self.headers, json=body)
        else:
            raise TypeError(f"The following HTTP method is not supported: {method}")

        if response.status_code >= 400:
            raise TypeError(f"Request produced a {response.status_code} - {response.reason}\n" + response.text)

        return response