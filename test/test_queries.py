import pytest

from anilistpy.anilist import Client, asMedia, asCharacter
from anilistpy.constants import manga, anime
from anilistpy.query_builder import QueryBuilder, PageQuery, MediaQuery, CharacterQuery

from anilistpy.wrappers.media import MediaSort

from .helpers import GqlClient

client = Client(GqlClient())
client.queries = {
    "mediaById": "media_by_id_body",
    "mediaListByIds": "media_list_by_ids_body",
    "mediaByName": "media_by_name_body"
}

# Query Builder Tests
def test_query_builder_can_build_simple_query_with_one_argument():
    query_builder = QueryBuilder()
    media_query = MediaQuery([("id", -1)])
    media_query.body = "body"
    query, variables = query_builder.build(media_query)

    assert query == "query($id:Int){Media(id:$id){body}}" and len(variables) == 1 and variables == { "id": -1 }

def test_query_builder_can_build_simple_query_with_multiple_arguments():
    query_builder = QueryBuilder()
    media_query = MediaQuery([
        ("id", -1),
        ("type", manga),
        ("chapters_greater", 1)
    ])
    media_query.body = "body"
    query, variables = query_builder.build(media_query)

    assert query == "query($id:Int,$type:MediaType,$chapters_greater:Int){Media(id:$id,type:$type,chapters_greater:$chapters_greater){body}}" and len(variables) == 3 and variables == { "id": -1, "type": manga, "chapters_greater": 1 }

def test_query_builder_raises_exception_when_multiple_keys_of_same_type_are_passed():
    query_builder = QueryBuilder()
    media_query = MediaQuery()
    with pytest.raises(KeyError):
        media_query.setArguments([
            ("id", 1),
            ("id", 2)
        ])

def test_query_builder_can_build_nested_query():
    query_builder = QueryBuilder()
    media_query = MediaQuery([
        ("id_in", [1, 2])
    ])
    media_query.body = "body"
    page_query = PageQuery(None, media_query)
    query, variables = query_builder.build(page_query)

    assert query == "query($id_in:[Int]){Page{media(id_in:$id_in){body}}}" and variables == { "id_in": [1,2] }

# Media Query Tests
def test_query_builder_can_build_media_query():
    query_builder = QueryBuilder()
    media_query = MediaQuery([
        ("id", 2966)
    ])
    media_query.body = "body"
    query, variables = query_builder.build(media_query)
    assert query == "query($id:Int){Media(id:$id){body}}" and variables == { "id": 2966 }

def test_query_builder_can_build_build_nested_media_query():
    query_builder = QueryBuilder()
    media_query = MediaQuery([
        ("id_in", [2966, 5341])
    ])
    media_query.body = "body"
    page_query = PageQuery(None, media_query)
    query, variables = query_builder.build(page_query)
    assert query == "query($id_in:[Int]){Page{media(id_in:$id_in){body}}}" and variables == { "id_in": [ 2966, 5341 ] }

def test_client_can_build_media_object():
    query_builder = QueryBuilder()
    media_query = MediaQuery([
        ("id", 2966)
    ])
    media_query.body = "body"
    query, variables = query_builder.build(media_query)
    media = asMedia(client.request(query, variables)["Media"])
    assert media.title.english() == "Spice and Wolf"

# Character Query Tests
def test_query_builder_can_build_character_query():
    query_builder = QueryBuilder()
    character_query = CharacterQuery([
        ("id", 7373)
    ])
    character_query.body = "body"
    query, variables = query_builder.build(character_query)
    assert query == "query($id:Int){Character(id:$id){body}}" and variables == { "id": 7373 }

def test_query_builder_can_build_build_nested_character_query():
    query_builder = QueryBuilder()
    character_query = CharacterQuery([
        ("id_in", [7373, -1])
    ])
    character_query.body = "body"
    page_query = PageQuery(None, character_query)
    query, variables = query_builder.build(page_query)
    assert query == "query($id_in:[Int]){Page{characters(id_in:$id_in){body}}}" and variables == { "id_in": [ 7373, -1 ] }

def test_client_can_build_character_object():
    query_builder = QueryBuilder()
    character_query = CharacterQuery([
        ("id", 7373)
    ])
    character_query.body = "body"
    query, variables = query_builder.build(character_query)
    character = asCharacter(client.request(query, variables)["Character"])
    assert character.name.first == "Holo"
