class CharacterName:
    def __init__(self, first, last, full, native):
        self.first = first
        self.last = last
        self.full = full
        self.native = native

class CharacterImage:
    def __init__(self, large, medium):
        self.large = large
        self.medium = medium

class Character():
    def __init__(self, id, name: CharacterName, image: CharacterImage, description, isFavourite, siteUrl, media, favourites):
        self.id = id
        self.name = name
        self.image = image
        self.description = description
        self.isFavourite = isFavourite
        self.siteUrl = siteUrl
        self.media = media
        self.favourites = favourites