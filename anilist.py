import requests, datetime
from gqlclient import GqlClient
import constants

import json, os, os.path

from collections import namedtuple
from wrappers.media import Media

class Client:

    def __init__(self):
        self.client = GqlClient(constants.url)
        self.queries = {
            "animeById": read("graphql\\anime_by_id.gql")
        }

    def getAnime(self, id: int):
        response = self.client.request(self.queries["animeById"], { "id": id, "type": "ANIME" })         
        return asAnime(response.json())

def read(relFilePath):
    absPath = os.path.abspath(os.path.dirname(__file__))
    absPath = os.path.join(absPath, relFilePath)

    with open(absPath) as file:
        contents = file.read()
    return contents

def asAnime(dct):
    data = dct["data"]["Media"]
    return Media(
        data["id"],
        asTitle(data["title"]),
        asDate(data["startDate"]),
        asDate(data["endDate"]),
        data["type"],
        data["format"],
        data["status"],
        data["description"],
        data["season"],
        data["seasonInt"],
        data["episodes"],
        data["duration"],
        data["countryOfOrigin"],
        data["isLicensed"],
        data["source"],
        data["hashtag"],
        data["updatedAt"],
        data["genres"],
        data["synonyms"],
        data["averageScore"],
        data["meanScore"],
        data["popularity"],
        data["isLocked"],
        data["trending"],
        data["favourites"],
        data["isFavourite"],
        data["isAdult"],
        data["streamingEpisodes"],
        data["siteUrl"],
        data["autoCreateForumThread"],
        data["isRecommendationBlocked"],
        data["airingSchedule"])

def asDate(dct):
    '''
    Takes a dictionary and returns a date object using the values.
    If either key has a None value, return None.
    '''
    if dct["year"] == None or dct["month"] == None or dct["day"] == None:
        return None
    return datetime.date(dct["year"], dct["month"], dct["day"])

def asTitle(dct):
    return {
        "romaji": dct["romaji"],
        "english": dct["english"],
        "native": dct["native"],
        "userPreferred": dct["userPreferred"]
    }

c = Client()
anime = c.getAnime(105310)
print(anime.title["romaji"])