import sys
from unittest.mock import patch

import pytest

from leetcode import pyleet


@pytest.mark.parametrize(
    ('filename',),
    (
        ('best_time_to_buy_and_sell_stock_alt.py',),
        ('design_linked_list.py',),
        ('height_checker.py',),
        ('intersection_of_two_arrays_ii.py',),
    ),
)
def test_pyleet_passing(filename, capsys):
    with patch.object(sys, 'argv', ['pyleet', f'testfiles/{filename}']):
        pyleet()

    captured = capsys.readouterr()
    outlines = (line.lower() for line in captured.out.splitlines())
    for line in outlines:
        assert 'passed' in line


@pytest.mark.parametrize(
    ('filename',),
    (
        ('group_anagrams.py',),
        ('jump_game.py',),
    ),
)
def test_pyleet_failing(filename, capsys):
    with patch.object(sys, 'argv', ['pyleet', f'testfiles/{filename}']):
        pyleet()

    stdout, _ = capsys.readouterr()
    stdout = stdout.lower()
    assert 'failed' in stdout
    assert 'errors:' in stdout
