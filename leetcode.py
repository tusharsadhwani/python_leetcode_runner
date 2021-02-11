"""
Python Leetcode runner

A CLI app to run any given Leetcode python solution.

Usage:
    pyleet remove_duplicates.py
"""
import sys
from typing import Any, Callable


def pyleet() -> int:
    """CLI interface."""

    if len(sys.argv) < 2:
        print('Error: No filename provided')
        return 1

    filename = sys.argv[1]
    return run_leetcode_solution(filename)


def run_leetcode_solution(filename: str) -> int:
    """Runs the leetcode solution file"""
    try:
        sys.path.append('.')
        module_name = filename.removesuffix('.py')
        module = __import__(module_name)
    except ModuleNotFoundError:
        print(f'Error: Unable to import file: {filename}')
        return 1

    if not hasattr(module, 'Solution'):
        print(f'Error: No Solution class found in file: {filename}')
        return 1

    solution_class = getattr(module, 'Solution')
    method_names = [name for name in dir(solution_class)
                    if not name.startswith('_')]

    if len(method_names) == 0:
        print('Error: No methods found inside Solution class')
        return 1

    if len(method_names) > 1:
        print('Error: Make sure you only put one method inside Solution class')
        return 1

    method_name, = method_names
    method = getattr(solution_class(), method_name)

    if not hasattr(module, 'tests'):
        print(f'Error: No tests found in file: {filename}')
        return 1

    tests = getattr(module, 'tests')

    if hasattr(module, 'validator'):
        validator = getattr(module, 'validator')
    else:
        def validator(
                method: Callable[..., Any],
                inputs: tuple[Any, ...],
                expected: tuple[Any, ...]) -> None:
            assert method(*inputs) == expected

    for index, (inputs, expected) in enumerate(tests):
        try:
            validator(method, inputs, expected)
            result = 'PASSED'
        except AssertionError:
            result = 'FAILED'

        inputs_string = ', '.join(str(i) for i in inputs)
        print(f"Case {index} - ({inputs_string}) - {result}")

    return 0