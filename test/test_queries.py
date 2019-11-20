import pytest

from anilistpy.anilist import Client, asMedia
from anilistpy.constants import manga, anime
from anilistpy.query_builder import QueryBuilder, PageQuery, MediaQuery

# TODO: Rewrite Tests to not trigger a network request
#       - Create a subclass of Client, that has a local storage for some mock data
#       - Overwrite SimpleQuery.body in tests, so we can more easily troubleshoot query problems
#       - These unit tests should focus on the syntax of tests

# TODO: Write unit tests for the following cases (and fix them in the code)
#       - Test when creating a query and passing it multiple arguments of the same type, the arguments
#           - ...should be condensed into one, so that we only focus on the first occourance of an argument
#           - ...shouldn't be accepted, and the query should raise an exception

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

c = Client()
def test_query_single_anime_by_id():
    assert c.getMediaById(2966).title.english() == "Spice and Wolf"

def test_query_single_anime_by_name():
    assert c.getMediaByName("Spice And Wolf").title.english() == "Spice and Wolf"

def test_query_multiple_anime_by_ids():
    animeList = c.getMediaListByIds([2966, 5341])
    assert len(animeList) == 2 and animeList[0].title.english() == "Spice and Wolf" and animeList[1].title.english() == "Spice and Wolf II"

def test_query_single_manga_by_id():
    assert c.getMediaById(33299, "MANGA").title.english() == "Spice & Wolf"

def test_query_single_manga_by_name():
    assert c.getMediaByName("Spice & Wolf", manga).title.english() == "Spice & Wolf"

def test_query_multiple_manga_by_ids():
    mangaList = c.getMediaListByIds([33299, 80767], manga)
    assert len(mangaList) == 2 and mangaList[0].title.english() == "Spice & Wolf" and mangaList[1].title.english() == "Real Girl"

###############################

def test_query_builder_can_build_simple_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id", 2966),
        ("type", anime),
        ("startDate_greater", 1)
    ])
    query, variables = qb.build(mq)

    media = asMedia(c.request(query, variables)["Media"])
    assert media.title.english() == "Spice and Wolf"

def test_query_builder_can_build_nested_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("type", anime),
        ("id_in", [2966, 5341])
    ])
    pq = PageQuery(None, mq)
    query, variables = qb.build(pq)

    print (query)
    print (variables)

    req = c.request(query, variables)
    mediaList = [asMedia(x) for x in req["Page"]["media"]]
    assert len(mediaList) == 2 and mediaList[0].title.english() == "Spice and Wolf" and mediaList[1].title.english() == "Spice and Wolf II"
