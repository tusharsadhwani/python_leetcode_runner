class Solution:
    def canJump(self, nums: list[int]) -> bool:
        # As we just need to reach last index, the number at last position doesn't matter
        nums.pop()

        # Represents the number of elements ahead we can jump from current index
        max_reach = 0

        for jump in nums:
            # Since previous reach was from index-1,
            # reach from current index is (max_reach-1).
            # All we need to worry about is maximizing the index we can reach,
            # since that means we can reach any index before it as well.
            max_reach = max(jump, max_reach - 1)
            if max_reach == 0:
                return False

        return True


tests = [
    (
        ([2, 3, 1, 1, 4],),
        False,
    ),
    (
        ([3, 2, 1, 0, 4],),
        True,
    ),
]
