"""
Python Leetcode runner

A CLI app to run any given Leetcode python solution.

Usage:
    pyleet remove_duplicates.py
"""
import sys


def pyleet() -> int:
    """CLI interface."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = sys.stdin.read()

    return run_leetcode_solution(filename)


def run_leetcode_solution(filename: str) -> int:
    """Runs the leetcode solution file"""
    try:
        with open(filename) as file:
            exec(file.read())  # pylint: disable=exec-used

        if 'Solution' not in locals():
            print(f'Error: No Solution class found in file: {filename}')
            return 1

        solution_class = locals()['Solution']
        function_name = dir(solution_class)[-1]
        if function_name.startswith('_'):
            print('Error: No function found inside Solution class')
            return 1

        function = solution_class.__dict__[function_name]
        function(solution_class())
    except FileNotFoundError:
        print(f'Error: Unable to open file: {filename}')
        return 1

    return 0
