class StaffName():
    def __init__(self, first, last, full, native):
        self.first = first
        self.last = last
        self.full = full
        self.native = native

class StaffImage():
    def __init__(self, large, medium):
        self.large = large
        self.medium = medium

class Staff():
    def __init__(self, id, name: StaffName, language, image, description, isFavourite, siteUrl, staffMedia,
        characters, staff, submitter, submissionStatus, submissionNotes, favourites):
        self.id = id
        self.name = name
        self.language = language
        self.image = image
        self.description = description
        self.isFavourite = isFavourite
        self.siteUrl = siteUrl
        self.staffMedia = staffMedia
        self.characters = characters
        self.staff = staff
        self.submitter = submitter
        self.submissionStatus = submissionStatus
        self.submissionNotes = submissionNotes
        self.favourites = favourites
