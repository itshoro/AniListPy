from graphene import ObjectType, Enum

class MediaStatus(ObjectType, Enum):
    Finished = "FINISHED"
    Airing = "AIRING"
    Upcoming = "UPCOMING"

# class MediaType(Enum):
#     Anime = "ANIME"
#     Manga = "MANGA"

# class Media(ObjectType):
#     id = Int()
#     mediaType = MediaType()


#     def __init__(self, id, mediaType, episode_amount):
#         self.id = id
#         self.mediaType = mediaType

#         self.title = Title()
#         self.episode_amount = episode_amount
#         self.episodes = []
        
#         # Todo: Query Episodes