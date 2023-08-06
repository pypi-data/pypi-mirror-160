from __future__ import annotations

import csv
import typing as t
from pathlib import Path


FilePath = Path | str


def _iter_dicxfile(
    dicx_filepath: FilePath,
) -> t.Generator[tuple[str, set[str]], None, None]:
    """Iterate over the lines of a dicx file."""
    with open(dicx_filepath) as buffer:
        reader = csv.reader(buffer)
        _, *category_names = next(
            reader
        )  # (e.g., DicTerm,PrivTtl,Intimacy,Law,NegativePrivacy,NormsRequisites)
        for line in reader:
            term_pattern, *categories = line
            category_set = {
                name for name, cat in zip(category_names, categories) if cat
            }
            yield term_pattern, category_set


def _search_trie(trie: Trie, token: str, token_i: int = 0) -> set[str] | None:
    """Search the given character-trie for paths that match the `token` string."""
    wildcard = trie.wildcard
    end = trie.end
    # if we hit a wildcard, we can stop
    if wildcard in trie:
        return trie[wildcard]  # type: ignore[no-any-return]

    # if we hit the end we can stop
    if end in trie and token_i == len(token):
        return trie[end]  # type: ignore[no-any-return]

    # recursion
    if token_i < len(token):
        char = token[token_i]
        token_i += 1
        if char in trie:
            return _search_trie(trie[char], token, token_i)

    return None


class Trie(t.Dict[str, t.Any]):
    """The Trie class is just a glorified dictionary.

    The only special addition is the method `search`, which
    searches the Trie for a given token or word. Additionally,
    the class can be called (i.e., __call__). The __call__
    method is just an alias for the search method.

    """

    def __init__(self, wildcard: str = "*", end: str = "$"):
        self.wildcard = wildcard
        self.end = end

    def search(self, token: str, token_i: int = 0) -> set[str] | None:
        """Search the Trie for the token."""
        return _search_trie(self, token, token_i)

    def __call__(self, token: str) -> set[str] | None:
        """Alias for the search method."""
        return self.search(token)

    @classmethod
    def from_dicx_file(
        cls, dicx_filepath: FilePath, wildcard_char: str, end_char: str
    ) -> Trie:
        """Create a Trie class from the LIWC .dicx file."""
        trie = cls(wildcard=wildcard_char, end=end_char)
        for pattern, categories in _iter_dicxfile(dicx_filepath):
            cursor = trie
            for char in pattern:
                if char == cursor.wildcard:
                    cursor[cursor.wildcard] = categories
                    break

                if char not in cursor:
                    cursor[char] = Trie(wildcard=wildcard_char, end=end_char)

                cursor = cursor[char]
            cursor[cursor.end] = categories
        return trie


def load_trie(
    dicx_filepath: FilePath, wildcard_char: str = "*", end_char: str = "$"
) -> Trie:
    """Create a Trie from a LIWC .dicx file."""
    return Trie.from_dicx_file(dicx_filepath, wildcard_char, end_char)
