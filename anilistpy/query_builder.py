class Query():
    def __init__(self, allowedArgs: list):
        self.allowedArgs = allowedArgs
        self.args = list()
        self.mediaBody = '''
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
        '''

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
                self.args.append((arg[0], filterTypes[filterNames.index(arg[0])], arg[1]))
                continue
            else:
                raise Exception("Filter not supported.")

    def getArgs(self):
        return self.args

class QueryBuilder:
    def __init__(self):
        pass

    def build(self, query):
        queryResult, queryVars = query.build()

        result = "query(" + ",".join([f"${arg[0]}:{arg[1]}" for arg in query.getArgs()]) + "){"
        result += queryResult
        result += "}"

        return result, queryVars

class MediaQuery(Query):
    def __init__(self, arguments):
        super().__init__([
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
            ("genre_in", NotImplemented),
            ("genre_not_in", NotImplemented),
            ("tag_in", NotImplemented),
            ("tag_not_in", NotImplemented),
            ("tagCategory_in", NotImplemented),
            ("tagCategory_not_in", NotImplemented),
            ("licensedBy_in", NotImplemented),
            ("averageScore_not", NotImplemented),
            ("averageScore_greater", NotImplemented),
            ("averageScore_lesser", NotImplemented),
            ("popularity_not", NotImplemented),
            ("popularity_greater", NotImplemented),
            ("popularity_lesser", NotImplemented),
            ("source_in", NotImplemented),
        ])
        super().setArguments(arguments)

    # Todo: Filter potentialArgs, so that only one instance of any argument is provided
    def build(self, mediaObject = "Media"):

        query = mediaObject
        if len(self.args):
            query += "(" + ",".join([f"{arg[0]}:${arg[0]}" for arg in self.args]) + ")"
        query += "{" + self.mediaBody +"}"

        variables =  {}
        for var in self.args:
            variables[var[0]] = var[2]

        return query, variables

class PageQuery(Query):
    def __init__(self, arguments: list, innerQuery: Query):
        super().__init__([
            ("Page", "Int"),
            ("perPage", "Int")
        ])
        if arguments != None:
            self.setArguments(arguments)
        self.innerQuery = innerQuery

    # TODO
    def build(self):
        innerQuery, innerVars = self.innerQuery.build("media")
        
        query = "Page"
        if len(self.args):
            query += "(" + ",".join([f"{arg[0]}:${arg[0]}" for arg in self.args]) + ")"
        query += "{" + innerQuery + "}"

        variables =  {}
        for var in self.args:
            variables[var[0]] = var[2]

        variables.update(innerVars)
        return query, variables

    def getArgs(self):
        fullArgumentList = super().getArgs()
        fullArgumentList.extend(self.innerQuery.getArgs())
        return fullArgumentList