from collections import Counter
from typing import Callable


class Solution:
    def intersect(self, nums1: list[int], nums2: list[int]) -> list[int]:
        num_counter = Counter(nums1)
        intersection: list[int] = []
        for num in nums2:
            if num_counter[num] > 0:
                intersection.append(num)
                num_counter[num] -= 1

        return intersection


tests = [
    (
        ([1, 2, 2, 1], [2, 2],),
        [2, 2],
    ),
    (
        ([4, 9, 5], [9, 4, 9, 8, 4],),
        [4, 9],
    ),
]


def validator(
    intersect: Callable[[list[int], list[int]], list[int]],
    inputs: tuple[list[int], list[int]],
    expected: list[int]
) -> None:
    nums1, nums2 = inputs
    output = intersect(nums1, nums2)
    assert len(output) == len(expected), (len(output), len(expected))
    assert set(output) == set(expected), (set(output), set(expected))
