# TODO: Implement sort in queries
# TODO: Find a consistent way on how to deal with edges in responses (list of ids and specifying the type in a doc string).

class QueryBuilder:
    def __init__(self):
        pass

    def build(self, query):
        queryResult, queryVars = query.build()

        result = "query(" + ",".join([f"${arg[0]}:{arg[1]}" for arg in query.getArgs()]) + "){"
        result += queryResult
        result += "}"

        return result, queryVars

class Query():
    def __init__(self, allowedArgs: list):
        self.allowedArgs = allowedArgs
        self.args = list()

    def build(self, potentialArgs = None):
        if potentialArgs != None:
            self.setArguments(potentialArgs)
        return self.args

    def getType(self, arg):
        return self.args[arg]

    def setArguments(self, potentialArgs: list):
        filterNames = [x[0] for x in self.allowedArgs]
        filterTypes = [x[1] for x in self.allowedArgs]
        self.args = []

        for arg in potentialArgs:
            if (arg[0] in filterNames):
                if (arg[0] not in [key[0] for key in self.args]):
                    self.args.append((arg[0], filterTypes[filterNames.index(arg[0])], arg[1]))
                    continue
                else:
                    raise KeyError(f"Invalid Mapping, argument \"{arg[0]}\" already set.")
            else:
                raise Exception("Filter not supported.")

    def getArgs(self):
        return self.args

class SimpleQuery(Query):
    def __init__(self, objectType: str, body: str, allowedArgs: list, queryArgs = None):
        super().__init__(allowedArgs)
        if queryArgs != None:
            super().setArguments(queryArgs)
        self.body = body
        self.objectType = objectType

    def build(self, args = None):
        if args != None:
            super().setArguments(args)

        result = self.objectType
        if len(self.args):
            result += "(" + ",".join([str(f"{arg[0]}:${arg[0]}") for arg in self.args]) + ")"
        result += f"{{{self.body}}}"

        variables =  {}
        for var in self.args:
            variables[var[0]] = var[2]

        return result, variables

class MediaQuery(SimpleQuery):
    def __init__(self, arguments = None):
        super().__init__(
            objectType = "Media",
            body = '''
            id
            endDate {
                year
                month
                day
            }
            airingSchedule {
                edges {
                    id
                    node {
                        id
                        airingAt
                        timeUntilAiring
                        episode
                        mediaId
                        media {
                            id
                        }
                    }
                }
            }
            title {
                romaji
                english
                native
                userPreferred
            }
            type
            format
            status
            description
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            season
            seasonInt
            episodes
            duration
            chapters
            volumes
            countryOfOrigin
            isLicensed
            source
            hashtag
            trailer {
                id
            }
            updatedAt
            coverImage {
                extraLarge
                large
                medium
                color
            }
            bannerImage
            genres
            synonyms
            averageScore
            meanScore
            popularity
            isLocked
            trending
            favourites
            tags {
                id
            }
            relations {
                edges {
                    id
                }
            }
            characters {
                edges {
                    id
                }
            }
            staff {
                edges {
                    id
                }
            }
            studios {
                edges {
                    id
                }
            }
            isFavourite
            isAdult
            nextAiringEpisode {
                id
            }
            trends {
                edges {
                    node {
                        averageScore
                        popularity
                        inProgress
                        episode
                    }
                }
            }
            externalLinks {
                id
            }
            streamingEpisodes {
                title
                thumbnail
                url
                site
            }
            rankings {
                id
            }
            mediaListEntry {
                id
            }
            reviews {
                edges {
                    node {
                        id
                    }
                }
            }
            recommendations {
                edges {
                    node {
                        id
                    }
                }
            }
            siteUrl
            autoCreateForumThread
            isRecommendationBlocked
            ''',
            allowedArgs = [
                ("id","Int"),
                ("id_not","[Int]"),
                ("id_in","[Int]"),
                ("id_not_in","[Int]"),
                ("startDate_greater", "FuzzyDateInt"),
                ("startDate_lesser", "FuzzyDateInt"),
                ("endDate_greater", "FuzzyDateInt"),
                ("endDate_lesser", "FuzzyDateInt"),
                ("episodes_greater", "Int"),
                ("episodes_lesser", "Int"),
                ("duration_greater", "Int"),
                ("duration_lesser", "Int"),
                ("chapters_greater", "Int"),
                ("chapters_lesser", "Int"),
                ("volumes_greater", "Int"),
                ("volumes_lesser", "Int"),
                ("type", "MediaType"),
                ("genre", "String"),
                ("genre_in", "[String]"),
                ("genre_not_in", "[String]"),
                ("tag", "String"),
                ("tag_in", "[String]"),
                ("tag_not_in", "[String]"),
                ("tagCategory", "String"),
                ("tagCategory_in", "[String]"),
                ("tagCategory_not_in", "[String]"),
                ("licensedBy_in", "String"),
                ("averageScroe", "Int"),
                ("averageScore_not", "Int"),
                ("averageScore_greater", "Int"),
                ("averageScore_lesser", "Int"),
                ("popularity", "Int"),
                ("popularity_not", "Int"),
                ("popularity_greater", "Int"),
                ("popularity_lesser", "Int"),
                ("source", "MediaSource"),
                ("source_in", "[MediaSource]"),
                ("sort", "[MediaSort]")
            ],
            queryArgs= arguments)

class CharacterQuery(SimpleQuery):
    def __init__(self, arguments = None):
        super().__init__(
            objectType="Character",
            body=
            '''
            id
            name {
                first
                last
                full
                native
            }
            image {
                large
                medium
            }
            description
            isFavourite
            siteUrl
            media {
                edges {
                    id
                }
            }
            favourites
            ''',
            allowedArgs = [
                ("id", "Int"),
                ("search", "String"),
                ("id_not", "Int"),
                ("id_in", "[Int]"),
                ("id_not_in", "[Int]"),
                ("sort", "CharacterSort")
            ],
            queryArgs=arguments
        )

class StaffQuery(SimpleQuery):
    def __init__(self, arguments: list):
        super().__init__(
            objectType = "Staff",
            body = '''
                id
                name {
                    first
                    last
                    full
                    native
                }
                language
                image {
                    large
                    medium
                }
                description
                isFavourite
                siteUrl
                staffMedia {
                    edges {
                        id
                    }
                }
                characters {
                    edges {
                        id
                    }
                }
                staff {
                    id
                }
                submitter {
                    id
                }
                submissionStatus
                submissionNotes
                favourites
            ''',
            allowedArgs = [
                ("id", "Int"),
                ("id_in", "[Int]"),
                ("search", "String"),
                ("id_not", "Int"),
                ("id_not_in", "[Int]"),
                ("sort", NotImplemented)
            ]
        )

class PageQuery(SimpleQuery):
    def __init__(self, arguments: list, innerQuery: Query):
        super().__init__(
            objectType = "Page",
            body = None,
            allowedArgs = [
                ("Page", "Int"),
                ("perPage", "Int")
            ], 
            queryArgs = arguments
        )
        if arguments != None:
            self.setArguments(arguments)
        self.innerQuery = innerQuery
        self.innerQuery.objectType = getNestedName(self.innerQuery.objectType)

    def build(self):
        innerQuery, innerVars = self.innerQuery.build()

        self.body = innerQuery
        query, variables = super().build()

        variables.update(innerVars)
        return query, variables

    def getArgs(self):
        fullArgumentList = super().getArgs()
        fullArgumentList.extend(self.innerQuery.getArgs())
        return fullArgumentList

# TODO Move this to constants, rename constants to something along the line of "lib_helpers"
def getNestedName(name: str):
    return {
        "Media": "media",
        "Character": "characters",
        "Staff": "staff"
    }[name]