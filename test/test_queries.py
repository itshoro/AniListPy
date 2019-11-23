import pytest

from anilistpy.anilist import Client, asMedia, asCharacter
from anilistpy.constants import manga, anime
from anilistpy.query_builder import QueryBuilder, PageQuery, MediaQuery, CharacterQuery

from .helpers import GqlClient

c = Client(GqlClient())
c.queries = {
    "mediaById": "media_by_id_body",
    "mediaListByIds": "media_list_by_ids_body",
    "mediaByName": "media_by_name_body"
}

# Query Builder Tests
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

def test_query_builder_raises_exception_when_multiple_keys_of_same_type_are_passed():
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

# Media Query Tests
def test_query_builder_can_build_media_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id", 2966)
    ])
    mq.body = "body"
    query, variables = qb.build(mq)
    assert query == "query($id:Int){Media(id:$id){body}}" and variables == { "id": 2966 }

def test_query_builder_can_build_build_nested_media_query():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id_in", [2966, 5341])
    ])
    mq.body = "body"
    pq = PageQuery(None, mq)
    query, variables = qb.build(pq)
    assert query == "query($id_in:[Int]){Page{media(id_in:$id_in){body}}}" and variables == { "id_in": [ 2966, 5341 ] }

def test_client_can_build_media_object():
    qb = QueryBuilder()
    mq = MediaQuery([
        ("id", 2966)
    ])
    mq.body = "body"
    query, variables = qb.build(mq)
    media = asMedia(c.request(query, variables)["Media"])
    assert media.title.english() == "Spice and Wolf"

# Character Query Tests
def test_query_builder_can_build_character_query():
    qb = QueryBuilder()
    cq = CharacterQuery([
        ("id", 7373)
    ])
    cq.body = "body"
    query, variables = qb.build(cq)
    assert query == "query($id:Int){Character(id:$id){body}}" and variables == { "id": 7373 }

def test_query_builder_can_build_build_nested_character_query():
    qb = QueryBuilder()
    cq = CharacterQuery([
        ("id_in", [7373, -1])
    ])
    cq.body = "body"
    pq = PageQuery(None, cq)
    query, variables = qb.build(pq)
    assert query == "query($id_in:[Int]){Page{characters(id_in:$id_in){body}}}" and variables == { "id_in": [ 7373, -1 ] }

def test_client_can_build_character_object():
    qb = QueryBuilder()
    cq = CharacterQuery([
        ("id", 7373)
    ])
    cq.body = "body"
    query, variables = qb.build(cq)
    character = asCharacter(c.request(query, variables)["Character"])
    assert character.name.first == "Holo"