import requests, datetime
import json, os, os.path

from .gqlclient import GqlClient
from .constants import url, anime, manga

from collections import namedtuple
from .wrappers.media import Media
from .wrappers.character import Character, CharacterImage, CharacterName
from .wrappers.title import MediaTitle

from .query_builder import MediaQuery

from functools import singledispatch
from typing import List

class Client:
    def __init__(self, client = None):
        self.client = client or GqlClient(url)
        # self.queries = {
        #     "mediaById": read("graphql\\media_by_id.gql"),
        #     "mediaListByIds": read("graphql\\media_list_by_ids.gql"),
        #     "mediaByName": read("graphql\\media_by_name.gql")
        # }

    # def getMediaById(self, id: int, type = anime) -> Media:
    #     return asMedia(self.request(self.queries["mediaById"], { "id": id, "type": type })["Media"])

    # def getMediaListByIds(self, ids: list, type = anime) -> list:
    #     # "Queries are allowed to return a maximum of 50 items. If this is exceeded you just won't receive more entries.
    #     response = self.request(self.queries["mediaListByIds"], { "id_in": ids, "type": type })
    #     return [asMedia(media) for media in response["Page"]["media"]]

    # def getMediaByName(self, name: str, type = anime) -> Media:
    #     return asMedia(self.request(self.queries["mediaByName"], { "name": name, "type": type })["Media"])

    # def getMedia(self, args: list) -> Media:
    #     mq = MediaQuery()
    #     query, variables = mq.build(args)
    #     # TODO: Consider a better method to pass the args to MediaQuery.build()
    #     # TODO: Create a QueryBuilder class, that chooses the right query class itself. (?)
    #     return asMedia(self.request(query, variables)["Media"])

    def request(self, query, variables):
        response = self.client.request(query, variables)
        return response["data"]

def read(relFilePath):
    absPath = os.path.abspath(os.path.dirname(__file__))
    absPath = os.path.join(absPath, relFilePath)

    with open(absPath) as file:
        contents = file.read()
    return contents

def asCharacter(data):
    return Character(
        data.get("id", None),
        asCharacterName(data.get("name", dict())),
        asCharacterImage(data.get("image", dict())),
        data.get("description", None),
        data.get("isFavourite", None),
        data.get("siteUrl", None),
        data.get("media", None),
        data.get("updatedAt", None),
        data.get("favourites", None)
    )

def asCharacterName(data):
    return CharacterName(
        data.get("first", None),
        data.get("last", None),
        data.get("full", None),
        data.get("native", None)
    )

def asCharacterImage(data):
    return CharacterImage(
        data.get("large",None),
        data.get("medium",None)
    )

def asMedia(data):
    return Media(
        data.get("id", None),
        asMediaTitle(data.get("title", dict())),
        asFuzzyDate(data.get("startDate", dict())),
        asFuzzyDate(data.get("endDate", dict())),
        data.get("type", None),
        data.get("format", None),
        data.get("status", None),
        data.get("description", None),
        data.get("season", None),
        data.get("seasonInt", None),
        data.get("episodes", None),
        data.get("duration", None),
        data.get("countryOfOrigin", None),
        data.get("isLicensed", None),
        data.get("source", None),
        data.get("hashtag", None),
        data.get("updatedAt", None),
        data.get("genres", None),
        data.get("synonyms", None),
        data.get("averageScore", None),
        data.get("meanScore", None),
        data.get("popularity", None),
        data.get("isLocked", None),
        data.get("trending", None),
        data.get("favourites", None),
        data.get("isFavourite", None),
        data.get("isAdult", None),
        data.get("streamingEpisodes", None),
        data.get("siteUrl", None),
        data.get("autoCreateForumThread", None),
        data.get("isRecommendationBlocked", None),
        data.get("airingSchedule", None))

def asFuzzyDate(dct: dict):
    '''
    Takes a dictionary and returns a date object using the values.
    If either key has a None value, return None.
    '''
    if dct.get("year", None) == None or dct.get("month", None) == None or dct.get("day", None) == None:
        return None
    return datetime.date(dct["year"], dct["month"], dct["day"])

def asMediaTitle(dct: dict):
    return MediaTitle(dct.get("romaji", None), dct.get("english", None), dct.get("native", None), dct.get("userPreferred", None))