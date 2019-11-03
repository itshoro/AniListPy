from graphene import ObjectType, List, ID, Int, Field
from episode import Episode

from media import Media

class AiringSchedule(ObjectType):
    id = ID()
    airingAt = Int()
    timeUntilAiring = Int()
    episode = Int()
    mediaId = Int()
    media = Field(Media())