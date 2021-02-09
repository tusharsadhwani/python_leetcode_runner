"""
Python Leetcode runner

A CLI app to run any given Leetcode python solution.

Usage:
    pyleet remove_duplicates.py
"""
import sys
from typing import Any


def pyleet() -> None:
    """CLI interface."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = sys.stdin.read()

    run_leetcode_solution(filename)


class Solution:
    """Dummy Solution class"""

    def noop(self, *args: Any, **kwargs: Any) -> None:
        """Dummy function"""
        raise Exception('No Solution class found')


def run_leetcode_solution(filename: str) -> None:
    """Runs the leetcode solution file"""
    try:
        with open(filename) as file:
            exec(file.read())

        function_name = dir(Solution)[-1]
        function = Solution.__dict__[function_name]
        function(Solution())
    except FileNotFoundError:
        print(f'Error: Unable to open file: {filename}')
        sys.exit(1)
