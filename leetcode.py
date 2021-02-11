"""
Python Leetcode runner

A CLI app to run any given Leetcode python solution.

Usage:
    pyleet remove_duplicates.py
"""
import os
import sys
from typing import Any, Callable

import color
from color import format_color, use_color


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
        validator = default_validator

    for index, (inputs, expected) in enumerate(tests, start=1):
        try:
            validator(method, inputs, expected)
            result = 'PASSED'
            result_color = color.GREEN
        except AssertionError:
            result = 'FAILED'
            result_color = color.RED

        test_case = f"Test {index} - ({', '.join(map(str, inputs))})"
        print_test_result(test_case, result, result_color)

    return 0


def default_validator(
        method: Callable[..., Any],
        inputs: tuple[Any, ...],
        expected: tuple[Any, ...]) -> None:
    """Default validator for leetcode tests"""
    assert method(*inputs) == expected


def print_test_result(test_case: str, result: str, clr: str) -> None:
    """Prints colored test result"""
    colored_result = colored(result, clr)
    apparent_padding = len(colored_result) - len(result)

    width, _ = os.get_terminal_size()
    test_case_width = len(test_case)
    rest_width = width - test_case_width + apparent_padding

    print(f'{test_case}{colored_result:.>{rest_width}}')


def colored(string: str, clr: str) -> str:
    """Returns colored string"""
    if use_color('auto'):
        return format_color(string, clr, True)

    return string
