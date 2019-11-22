import pytest

from anilistpy.anilist import Client, asMedia
from anilistpy.constants import manga, anime
from anilistpy.query_builder import QueryBuilder, PageQuery, MediaQuery

from .helpers import GqlClient

# TODO: Rewrite Tests to not trigger a network request ✔
#       - Create a subclass of Client, that has a local storage for some mock data ✔
#       - Overwrite SimpleQuery.body in tests, so we can more easily troubleshoot query problems ✔
#       - Rework tests so they focus on our implementation, instead of relying on data (the data we will receive has to be taken as correct, so there is no reason to test it) ✔

# TODO: Write unit tests for the following cases (and fix them in the code)
#       - Test when creating a query and passing it multiple arguments of the same type, the arguments ✔
#           - ~...should be condensed into one, so that we only focus on the latest occourance of an argument ~
#           - ...shouldn't be accepted, and the query should raise an exception ✔

# FIXME:Nested Queries (Page Queries) should take in more than one query
#       Right now Page Queries can only have *one* nested query. To give the user the highest customizability,
#       the PageQuery.innerQuery field should be a list of unique queries (and query types). This will force me to
#       rewrite how I'm assigning variable names, since there is some overlap in arguments, e.g.:
#
#       Current:
#       Media(id:$id), Character(id:$id)
#       vars = { "id": x, "id": y }
#
#       Proposed:
#       Media(id:$x), Character(id:$y)
#       vars = { "x": a, "y": b }

c = Client(GqlClient())
c.queries = {
    "mediaById": "media_by_id_body",
    "mediaListByIds": "media_list_by_ids_body",
    "mediaByName": "media_by_name_body"
}

def test_query_builder_can_build_simple_query_with_one_argument():
    qb = QueryBuilder()
    mq = MediaQuery([("id", -1)])
    mq.body = "body"
    query, variables = qb.build(mq)

    assert query == "query($id:Int){Media(id:$id){body}}" and len(variables) == 1 and variables == { "id": -1 }

def test_query_builder_can_build_simple_query_with_multiple_arguments():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id", -1),
        ("type", manga),
        ("chapters_greater", 1)
    ])
    mq.body = "body"
    query, variables = qb.build(mq)

    assert query == "query($id:Int,$type:MediaType,$chapters_greater:Int){Media(id:$id,type:$type,chapters_greater:$chapters_greater){body}}" and len(variables) == 3 and variables == { "id": -1, "type": manga, "chapters_greater": 1 }

# Maybe instead raise an exception or let the user decide. The default behavior is to just truncate the args.
def test_query_builder_truncates_multiple_arguments_of_the_same_type_into_one():
    qb = QueryBuilder()
    mq = MediaQuery()
    with pytest.raises(KeyError):
        mq.setArguments([
            ("id", 1),
            ("id", 2)
        ])

def test_query_builder_can_build_nested_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id_in", [1, 2])
    ])
    mq.body = "body"
    pq = PageQuery(None, mq)
    query, variables = qb.build(pq)

    assert query == "query($id_in:[Int]){Page{media(id_in:$id_in){body}}}" and variables == { "id_in": [1,2] }

def test_client_can_build_single_media():
    anime = c.getMediaById(2966)
    assert anime.title.english() == "Spice and Wolf"

def test_client_can_build_multiple_medias_by_list_of_ids():
    animeList = c.getMediaListByIds([2966, 5341])
    assert len(animeList) == 2 and animeList[0].title.english() == "Spice and Wolf" and animeList[1].title.english() == "Spice and Wolf II"

def test_client_can_request_media_by_built_simple_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id", 2966),
        ("type", anime),
        ("startDate_greater", 1)
    ])
    query, variables = qb.build(mq)

    media = asMedia(c.request(query, variables)["Media"])
    assert media.title.english() == "Spice and Wolf"

def test_client_can_request_list_of_media_by_built_nested_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("type", anime),
        ("id_in", [2966, 5341])
    ])
    pq = PageQuery(None, mq)
    query, variables = qb.build(pq)

    req = c.request(query, variables)
    mediaList = [asMedia(x) for x in req["Page"]["media"]]
    assert len(mediaList) == 2 and mediaList[0].title.english() == "Spice and Wolf" and mediaList[1].title.english() == "Spice and Wolf II"
