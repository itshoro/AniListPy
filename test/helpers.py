from anipy.gqlclient import GqlClient
from anipy.query_builder import getNestedName
import json
import math

class GqlClient(GqlClient):
    def __init__(self):
        self.data = {
            "Media": {
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
            },
            "Character": {
                7373:
                {
                    "Character":
                    {
                        "name": {
                            "first": "Holo"
                        }
                    }
                }
            },
            "Staff": {
                95070:
                {
                    "Staff": {
                        "id": 95070,
                        "name": {
                            "first": "Ami",
                            "last": "Koshimizu",
                            "full": "Ami Koshimizu",
                            "native": "小清水亜美"
                        }
                    }
                }
            }
        }

    def request(self, query, variables):
        amount = query.count('}')

        if amount == 2:
            positionOfType = query.index('{') + 1
            nextPos = min(
                query.index('{', positionOfType),
                query.index('(', positionOfType)
            )
            requestType = query[positionOfType : nextPos]
        else:
            pagePos = query.index('{')
            positionOfType = query.index('{', pagePos + 1) + 1
            nextPos = min(
                query.index('{', positionOfType),
                query.index('(', positionOfType)
            )
            requestType = query[positionOfType : nextPos]


        if "id" in variables:
            return {
                "data": self.data[requestType][variables["id"]]
            }
        elif "id_in" in variables:
            data = { "data" : { "Page": { getNestedName("Media"): [] } } }
            listData = []
            for id in variables["id_in"]:
                if id in self.data[requestType].keys():
                    listData.append(self.data[requestType][id]["Media"])
            data["data"]["Page"]["media"] = listData
            return data
        raise Exception()