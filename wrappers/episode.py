from graphene import ObjectType, String, List, Field, Int, ID

class MediaStreamingEpisode(ObjectType):
    title = String()
    thumbnail = String()
    url = String()
    site = String()

class Episode(ObjectType):
    id = ID()
    airingAt = Int()
    timeUntilAiring = Int()
    episode = Int()

# class Episode:
#     def __init__(self, id,episode_number, airing_at, mediaId):
#         self.id = id
#         self.episode_number = episode_number
#         self.airing_at = airing_at
#         self.mediaId = mediaId

#     def timeUntilAiring(self):
#         return self.airing_at - datetime.now().microsecond