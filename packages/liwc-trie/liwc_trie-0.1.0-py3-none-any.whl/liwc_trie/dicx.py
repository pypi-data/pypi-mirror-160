from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from itertools import chain
from pathlib import Path

from .trie import Trie
from .trie import load_trie


FilePath = Path | str


@dataclass
class LiwcDictionary:
    """Class representing a LIWC dictionary."""

    def __init__(self, dicx_file: FilePath):
        """Create a LiwcDictionary class.

        Args:
            dicx_file (FilePath): _description_
        """
        self._dicx_file = Path(dicx_file)
        self._info_file = self._dicx_file.with_suffix(".html")
        self.name = self._dicx_file.stem

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"

    @cached_property
    def _trie(self) -> Trie:
        return load_trie(self._dicx_file)

    def show_info(self) -> None:
        """Open the info HTML in the default web browser."""
        if self._info_file.exists():
            import webbrowser

            webbrowser.open(str(self._info_file))
        raise FileNotFoundError(f"{self._info_file} does not exist.")

    def get_liwc_counts(self, text: str) -> Counter[str]:
        """Count the number of occurences of each LIWC category in a given text."""
        tokens = (token.group().lower() for token in re.finditer(r"\w+", text))
        category_sets: filter[set[str]] = filter(None, map(self._trie.search, tokens))
        return Counter(chain.from_iterable(category_sets))


def load_liwc_dictionary(dicx_file: FilePath) -> LiwcDictionary:
    """Load a .dicx file.

    Args:
        dicx_file (FilePath): File containing LIWC dictionary data.

    Returns:
        LiwcDictionary: Class for parsing text with the LIWC dictionary data.
    """
    return LiwcDictionary(dicx_file)


__all__ = ["load_liwc_dictionary"]
