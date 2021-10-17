class Solution:
    def heightChecker(self, heights: list[int]) -> int:
        incorrect_count = 0

        expected = sorted(heights)
        for height, expected_height in zip(heights, expected):
            if height != expected_height:
                incorrect_count += 1

        return incorrect_count


tests = [
    (
        ([1, 1, 4, 2, 1, 3],),
        3,
    ),
    (
        ([5, 1, 2, 3, 4],),
        5,
    ),
    (
        ([1, 2, 3, 4, 5],),
        0,
    ),
]
