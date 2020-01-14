import requests, json

# We do client sided rate limiting, because I don't want to time out the user for 1 minute.
class RateLimitException(Exception):
    def __init__(msg):
        super().__init__(msg)

class GqlClient:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.rateLimitCurrent = self.setRateLimits(requests.post(self.url).headers)

    def setRateLimits(self, headers):
        self.rateLimitCurrent = headers.get("x-ratelimit-remaining")

    def request(self, query, variables = None):
        if (self.rateLimitCurrent <= 0):
            raise RateLimitException("Exceeded rate limit.")

        payload = { "query": query, "variables": variables }
        response = requests.post(self.url, headers=self.headers, json=payload)

        self.setRateLimits(response.headers)
        if response.status_code >= 400:
            raise TypeError(f"Request produced a {response.status_code} - {response.reason}\n" + response.text)

        return response.json()