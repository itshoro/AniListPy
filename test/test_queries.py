import pytest

from anilistpy.anilist import Client
from anilistpy.constants import manga

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

def test_query_builder():
    assert c.getMedia([
        ("id", 2966),
        ("type", "ANIME"),
        ("startDate_greater", 1)
    ]).title.english() == "Spice and Wolf"
