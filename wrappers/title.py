from graphene import ObjectType, String

class MediaTitle(ObjectType):
    romaji = String()
    english = String()
    native = String()
    userPreferred = String()