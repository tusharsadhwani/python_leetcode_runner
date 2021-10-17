from collections import Counter
from typing import Callable


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        anagrams: dict[frozenset[tuple[str, int]], list[str]] = {}

        for string in strs:
            counter = frozenset(Counter(string).items())
            if counter in anagrams:
                anagrams[counter].append(string)
            else:
                anagrams[counter] = [string]

        return list(anagrams.values())


tests = [
    (
        (["eat", "tea", "tan", "ate", "nat", "bat"],),
        [["bat"], ["nat", "tan"], ["ate", "eat"]],
    ),
    (
        ([''],),
        [['']],
    ),
    (
        (['a'],),
        [['a']],
    ),
]


def validator(
    groupAnagrams: Callable[[list[str]], list[list[str]]],
    inputs: tuple[list[str]],
    expected: list[list[str]],
) -> None:
    (strs,) = inputs
    output = groupAnagrams(strs)
    output_set = {frozenset(group) for group in output}
    expected_set = {frozenset(group) for group in expected}
    assert output_set == expected_set, (output_set, expected_set)
