import requests, datetime
from gqlclient import GqlClient
import constants

import json, os, os.path

from collections import namedtuple
from wrappers.media import Media
from wrappers.title import MediaTitle

from functools import singledispatch
from typing import List

class Client:

    def __init__(self):
        self.client = GqlClient(constants.url)
        self.queries = {
            "mediaById": read("graphql\\media_by_id.gql"),
            "mediasById": read("graphql\\medias_by_id.gql"),
            "mediaByName": read("graphql\\media_by_name.gql")
        }

    def getMediaById(self, id: int, type = "ANIME") -> Media:
        response = self.client.request(self.queries["mediaById"], { "id": id, "type": type })         
        return asMedia(response.json()["data"])

    def getMediasById(self, ids: List[int], type = "ANIME") -> List[Media]:
        response = self.client.request(self.queries["mediasById"], { "ids": ids, "count": len(ids), "type": type })         
        yield [asMedia(media) for media in response.json()["data"]["Page"]]

    def getMediaByName(self, name: str, type = "ANIME") -> Media:
        response = self.client.request(self.queries["mediaByName"], { "search": name, "type": type })         
        return asMedia(response.json()["data"])


def read(relFilePath):
    absPath = os.path.abspath(os.path.dirname(__file__))
    absPath = os.path.join(absPath, relFilePath)

    with open(absPath) as file:
        contents = file.read()
    return contents

def asMedia(dct):
    data = dct["Media"]
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
    return MediaTitle(dct["romaji"], dct["english"], dct["native"], dct["userPreferred"])

c = Client()
anime = c.getMediaById(105310)
print(anime.title)