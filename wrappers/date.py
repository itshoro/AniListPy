from graphene import Int, ObjectType

class FuzzyDate(ObjectType):
    year = Int()
    month = Int()
    day = Int()