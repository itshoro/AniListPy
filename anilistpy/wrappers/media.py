class MediaStreamingEpisode:
    def __init__(self, title, thumbnail, url, site):
        self.title = title
        self.thumbnail = thumbnail
        self.url = url
        self.site = site

class MediaTag:
    def __init__(self, id, name, description, category, rank, isGeneralSpoiler, isMediaSpoiler, isAdult):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.rank = rank
        self.isGeneralSpoiler = isGeneralSpoiler
        self.isMediaSpoiler = isMediaSpoiler
        self.isAdult = isAdult

class MediaExternalLink:
    def __init__(self, id, url, site):
        self.id = id
        self.url = url
        self.site = site

class MediaTrailer:
    def __init__(self, id, site, thumbnail):
        self.id = id
        self.site = site
        self.thumbnail = thumbnail

class AiringSchedule:
    def __init__(self, id, airingAt, timeUntilAiring, episode, mediaId):
        self.id = id
        self.airingAt = airingAt
        self.timeUntilAiring = timeUntilAiring
        self.episode = episode
        self.mediaId = mediaId

class MediaImage:
    def __init__(self, extraLarge, large, medium, color):
        self.extraLarge = extraLarge
        self.large = large
        self.medium = medium
        self.color = color

import os
class MediaTitle():
    def __init__(self, romaji, english, native, userPreferred):
        self.romaji = romaji
        self.english = english
        self.native = native
        self.userPreferred = userPreferred

    def __str__(self):
        return f"[romaji]: {self.romaji}{os.linesep}[english]: {self.english}{os.linesep}[native]: {self.native}{os.linesep}[userPreferred]: {self.userPreferred}"

class Media:
    def __init__(self, airingSchedule, id, title, startDate, endDate, type, format, status, description, season, seasonInt, episodes, duration, chapters, volumes, countryOfOrigin, isLicensed,
    source, hashtag, trailer, updatedAt, coverImage, bannerImage, genres, synonyms, averageScore, meanScore, popularity, isLocked, trending, favourites, tags, relations, characterIds, staffIds, studios, isFavourite, isAdult, nextAiringEpisode, trends, externalLinks, streamingEpisodes,
    rankings, mediaListEntry, reviews, recommdations, siteUrl, autoCreateForumThread, isRecommendationBlocked):
        self.airingSchedule = airingSchedule
        self.id = id
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.type = type
        self.format = format
        self.status = status
        self.description = description
        self.season = season
        self.seasonInt = seasonInt
        self.episodes = episodes
        self.duration = duration
        self.chapters = chapters
        self.volumes = volumes
        self.countryOfOrigin = countryOfOrigin
        self.isLicensed = isLicensed
        self.source = source
        self.hashtag = hashtag
        self.trailer = trailer
        self.updatedAt = updatedAt
        self.coverImage = coverImage
        self.bannerImage = bannerImage
        self.genres = genres
        self.synonyms = synonyms
        self.averageScore = averageScore
        self.meanScore = meanScore
        self.popularity = popularity
        self.isLocked = isLocked
        self.trending = trending
        self.favourites = favourites
        self.tags = tags
        self.relarelations =relations
        self.characterIds = characterIds
        self.staffIds = staffIds
        self.studios = studios
        self.isFavourite = isFavourite
        self.isAdult = isAdult
        self.nextAiringEpisode = nextAiringEpisodes
        self.trends = trends
        self.externalLinks = externalLinks
        self.streamingEpisodes = streamingEpisodes
        self.rankings = rankings
        self.mediaListEntry = mediaListEntry
        self.reviews = reviews
        self.recommendations = recommendations
        self.siteUrl = siteUrl
        self.autoCreateForumThread = autoCreateForumThread
        self.isRecommendationBlocked = isRecommendationBlocked
