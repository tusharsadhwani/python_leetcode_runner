"""
Python Leetcode runner

A CLI app to run any given Leetcode python solution.

Usage:
    pyleet remove_duplicates.py
"""
import os
import sys
from traceback import extract_tb
from types import TracebackType
from typing import Any, Callable, Optional

import color
from color import format_color, use_color


def pyleet() -> int:
    """CLI interface."""

    if len(sys.argv) < 2:
        print_error('No filename provided')
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
        print_error(f'Unable to import file: {filename}')
        return 1

    if not hasattr(module, 'Solution'):
        print_error(f'No Solution class found in file: {filename}')
        return 1

    solution_class = getattr(module, 'Solution')
    method_names = [name for name in dir(solution_class)
                    if not name.startswith('_')]

    if len(method_names) == 0:
        print_error('No methods found inside Solution class')
        return 1

    if len(method_names) > 1:
        print_error('Make sure you only put one method inside Solution class')
        return 1

    method_name, = method_names
    method = getattr(solution_class(), method_name)

    if not hasattr(module, 'tests'):
        print_error(f'No tests found in file: {filename}')
        return 1

    tests = getattr(module, 'tests')

    if hasattr(module, 'validator'):
        validator = getattr(module, 'validator')
    else:
        validator = default_validator

    failed_testcases = run_testcases(method, tests, validator)

    if len(failed_testcases) == 0:
        success_color = color.BOLD + color.SUCCESS
        print_colored('All cases passed!', clr=success_color)
    else:
        print_failed_testcases(failed_testcases)

    return 0


def default_validator(
        method: Callable[..., Any],
        inputs: tuple[Any, ...],
        expected: tuple[Any, ...]) -> None:
    """Default validator for leetcode tests"""
    output = method(*inputs)
    assert output == expected, (output, expected)


def run_testcases(
    method:  Callable[..., Any],
    tests: list[tuple[Any, Any]],
    validator: Any,
) -> list[tuple[TracebackType, Any, Any, Any]]:
    """Run given test cases, and collect all failing assertions"""
    failed_testcases: list[tuple[TracebackType, Any, Any, Any]] = []

    for index, (inputs, expected) in enumerate(tests, start=1):
        try:
            validator(method, inputs, expected)
            result = 'PASSED'
            result_color = color.GREEN + color.BOLD
        except AssertionError as exc:
            *_, trace = sys.exc_info()
            assert trace is not None

            if len(exc.args) != 1:
                raise ValueError(
                    "No assertion value provided in custom validator"
                ) from exc

            assertion_values, = exc.args
            if len(assertion_values) != 2:
                raise ValueError(
                    "Assertion value must be provided as (output, expected)"
                ) from exc

            result = 'FAILED'
            result_color = color.RED + color.BOLD
            output, expected = assertion_values
            failed_testcases.append((trace, inputs, expected, output))

        test_case = f"Test {index} - ({', '.join(map(str, inputs))})"
        print_test_result(test_case, result, result_color)

    return failed_testcases


def print_failed_testcases(
        failed_testcases: list[tuple[TracebackType, Any, Any, Any]]
) -> None:
    """Prints failed test cases"""
    err_color = color.BOLD + color.ERROR

    print_colored('Errors:', clr=err_color)
    for traceback, inputs, expected, output in failed_testcases:
        inputs_string = ', '.join(map(str, inputs))
        assertion = get_assert_statement(traceback)

        print()
        print_colored('Inputs:', inputs_string, clr=err_color)
        print_colored('Assertion:', assertion, clr=err_color)
        print_colored('Expected:', expected, clr=err_color)
        print_colored('Output:', output, clr=err_color)


def print_test_result(test_case: str, result: str, clr: str) -> None:
    """Prints colored test result"""
    colored_result = colored(result, clr)
    apparent_padding = len(colored_result) - len(result)

    width, _ = os.get_terminal_size()
    test_case_width = len(test_case)
    if test_case_width > width - len(result) - 3:
        test_case_width = width - len(result) - 3
        test_case = test_case[:test_case_width]

    rest_width = width - test_case_width + apparent_padding

    print(f'{test_case}{colored_result:.>{rest_width}}')


def get_assert_statement(traceback: Any) -> str:
    """Gets the line of code that the assertion came from"""
    tb_info = extract_tb(traceback)
    *_, text = tb_info[-1]
    return str(text)


def colored(string: str, clr: str) -> str:
    """Returns colored string"""
    if use_color('auto'):
        return format_color(string, clr, True)

    return string


def print_colored(
    *values: Any,
    clr: Optional[str] = None,
    sep: str = ' ',
    end: str = '\n'
) -> None:
    """Print, but colored"""
    text = sep.join(map(str, values)) + end

    if clr:
        text = colored(text, clr)

    print(text, end='')


def print_error(string: str) -> None:
    """Prints an error"""
    error = colored('Error:', color.ERROR + color.BOLD)
    print(error, string)
