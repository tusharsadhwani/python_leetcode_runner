import sys


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        # If there's a new lowest value that you could've bought at,
        # you don't need to care about the previous lowest value ahead.
        lowest = sys.maxsize
        max_profit = 0
        for price in prices:
            if price < lowest:
                lowest = price

            profit = price - lowest
            max_profit = max(max_profit, profit)

        return max_profit


tests = [
    (
        ([7, 1, 5, 3, 6, 4],),
        5,
    ),
    (
        ([7, 6, 4, 3, 1],),
        0,
    )
]
