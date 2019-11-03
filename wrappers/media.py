from graphene import ID, String, Int, Boolean, Field, List, ObjectType

from title import MediaTitle
from airingSchedule import AiringSchedule
from status import MediaStatus

from episode import MediaStreamingEpisode

from date import FuzzyDate

class Media(ObjectType):
    id = ID()
    title = Field(MediaTitle)
    startDate = Field(FuzzyDate)
    endDate = Field(FuzzyDate)

    type = String()
    format = String()
    status = String()
    description = String()
    season = String()
    seasonInt = Int()
    episodes = Int()
    duration = Int()
    countryOfOrigin = String()
    isLicensed = Boolean()
    source = String()
    hashtag = String()
    updatedAt = String()
    genres = List(String())
    synonyms = List(String())
    averageScore = Int()
    meanScore = Int()
    popularity = Int()
    isLocked = Boolean()
    trending = Int()
    favourites = Int()
    isFavourite = Boolean()
    isAdult = Boolean()
    streamingEpisodes = List(MediaStreamingEpisode())
    siteUrl = String()
    autoCreateForumThread = Boolean()
    isRecommendationBlocked = Boolean()

    episodes = Field(AiringSchedule)
    status = Field(MediaStatus)

    # TODO: modNotes, reviews, rankings, mediaListEntry, externalLink, trends, nextAiringEpisode, chapters, volumes, trailer, coverimage, bannerimage, tags, relations, characters, staff, studios, 