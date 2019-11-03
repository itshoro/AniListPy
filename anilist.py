import requests, datetime

class Preferences:
    preferredTitle = "romaji"

class Anime:
    title = {
        "romaji": "",
        "english": "",
        "native": ""
    }
    totalEpisodeCount = 0
    currentEpisode = 0

    nextEpisodeAiringIn = -1

    def toString(self, preferences):
        return f"{self.title[preferences.preferredTitle]}: is airing in {str(self.nextEpisodeAiringIn - datetime.datetime.utcnow())}"



def requestAnimeInformationFromId(id):
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
    Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        title {
        romaji
        english
        native
        }
    }
    }
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        'id': id
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})
    print(response.text)

requestAnimeFromId(2966)