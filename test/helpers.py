from anilistpy.gqlclient import GqlClient
from anilistpy.query_builder import getNestedName
import json

class GqlClient(GqlClient):
    def __init__(self):
        self.data = {
            "ANIME": {
                2966: 
                {
                    "Media": 
                    {
                        "title": 
                        {
                            "english": "Spice and Wolf"
                        }
                    }
                },
                5341: 
                {
                    "Media": {
                        "id": 5341,
                        "title": 
                        {
                            "english": "Spice and Wolf II"
                        }
                    }
                }
            }
        }

    def request(self, query, variables):
        if "id" in variables:
            return {
                "data": self.data[variables["type"]][variables["id"]]
            }
        elif "id_in" in variables:
            data = { "data" : { "Page": { getNestedName("Media"): [] } } }
            listData = []
            for id in variables["id_in"]:
                if id in self.data[variables["type"]].keys():
                    listData.append(self.data[variables["type"]][id]["Media"])
            data["data"]["Page"]["media"] = listData
            return data
        raise Exception()