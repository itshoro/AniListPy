import requests, datetime
import json, os, os.path

from .gqlclient import GqlClient
from .constants import url, anime, manga

from collections import namedtuple
from .wrappers.media import Media, MediaTitle, AiringSchedule, MediaTrailer, MediaImage, MediaTag, MediaExternalLink, MediaStreamingEpisode
from .wrappers.character import Character, CharacterImage, CharacterName

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

def asMediaTrailer(data: dict):
    return MediaTrailer(
        data.get("id", None),
        data.get("site", None),
        data.get("thumbnail", None)
    )

def asMediaTag(data):
    return MediaTag(
        data.get("id", None),
        data.get("name", None),
        data.get("description", None),
        data.get("category", None),
        data.get("rank", None),
        data.get("isGeneralSpoiler", None),
        data.get("isMediaSpoiler", None),
        data.get("isAdult", None)
    )

def asMediaExternalLink(data):
    return MediaExternalLink(
        data.get("id", None),
        data.get("url", None),
        data.get("site", None)
    )

def asMediaStreamingEpisode(data):
    return MediaStreamingEpisode(
        data.get("title", None),
        data.get("thumbnail", None),
        data.get("url", None),
        data.get("site", None)
    )

def asMedia(data):
    return Media(
        [asAiringSchedule(airingScheduleDate) for airingScheduleDate in data.get("airingSchedule", dict()).get("edges", dict())],
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
        data.get("chapters", None),
        data.get("volumes", None),
        data.get("countryOfOrigin", None),
        data.get("isLicensed", None),
        data.get("source", None),
        data.get("hashtag", None),
        asMediaTrailer(data.get("trailer", dict())),
        data.get("updatedAt", None),
        asMediaImage(data.get("coverImage", dict())),
        data.get("bannerImage", None),
        data.get("genres", None),
        data.get("synonyms", None),
        data.get("averageScore", None),
        data.get("meanScore", None),
        data.get("popularity", None),
        data.get("isLocked", None),
        data.get("trending", None),
        data.get("favourites", None),
        [asMediaTag(tag) for tag in data.get("tags", dict())],
        [relationId for relationId in data.get("relations", dict()).get("edges", dict())],
        [charId for charId in data.get("characters", dict()).get("edges", dict())],
        [staffId for staffId in data.get("staff", dict()).get("edges", dict())],
        [studioId for studioId in data.get("studios", dict()).get("edges", dict())],
        data.get("isFavourite", None),
        data.get("isAdult", None),
        asAiringSchedule(data.get("nextAiringEpisode", dict())),
        data.get("trends", None), # TODO: Parse MediaTrends
        [asMediaExternalLink(link) for link in data.get("externalLinks", dict())],
        [asMediaStreamingEpisode(episode) for episode in data.get("streamingEpisodes", dict())],
        data.get("rankings", None), # TODO: Parse MediaRankings
        data.get("mediaListEntry", None), # TODO: Parse this, **if** the user is authenticated, TODO: Make it able so users are able to authenticate
        data.get("reviews", None), # TODO: Parse Reviews. Maybe just keep these as ids and query them seperately
        data.get("recommendations", None), # TODO: Parse Recommendations
        data.get("siteUrl", None),
        data.get("autoCreateForumThread", None),
        data.get("isRecommendationBlocked", None))

def asMediaImage(data):
    return MediaImage(
        data.get("extraLarge", None),
        data.get("large", None),
        data.get("medium", None),
        data.get("color", None)
    )

def asAiringSchedule(dct: dict):
    return AiringSchedule(dct.get("id", None), dct.get("airingAt", None), dct.get("tileUntilAiring", None), dct.get("episode", None), dct.get("mediaId", None))

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