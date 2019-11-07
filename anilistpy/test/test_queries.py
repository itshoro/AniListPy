import pytest
from anilistpy.anilist import Client

c = Client()

def test_query_single_anime_by_id():
    assert c.getMediaById(2966).title.english() == "Spice and Wolf"

def test_query_single_anime_by_name():
    assert c.getMediaByName("Spice And Wolf").title.english() == "Spice and Wolf"

def test_query_multiple_anime_by_ids():
    animeList = c.getMediaListByIds([2966, 5341])
    [print(anime.title) for anime in animeList]
    assert len(animeList) == 2 and animeList[0].title.english() == "Spice and Wolf" and animeList[1].title.english() == "Spice and Wolf II"