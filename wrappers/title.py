import os
class MediaTitle():
    def __init__(self, romaji, english, native, userPreferred):
        self._romaji = romaji
        self._english = english
        self._native = native
        self._userPreferred = userPreferred

    def __str__(self):
        return f"[romaji]: {self._romaji}{os.linesep}[english]: {self._english}{os.linesep}[native]: {self._native}{os.linesep}[userPreferred]: {self._userPreferred}"

    def romaji(self):
        return self._romaji

    def english(self):
        return self._english

    def native(self):
        return self._native

    def userPreferred(self):
        return self._userPreferred