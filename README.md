# python_leetcode_runner

Test your leetcode Python solutions locally.

![demo image](https://user-images.githubusercontent.com/43412083/107806692-2b58fa80-6d8d-11eb-9b4b-137ca9792476.png)

## Installation

```console
pip install python-leetcode-runner
```

## Usage

Say your solution file `add_numbers.py` looks like this:

```python
class Solution:
    def addNumbers(self, nums: list[int]) -> int:
        return sum(nums)
```

All you need to add to the file is a few test cases, usually provided to you in the leetcode question description:

```python
class Solution:
    def addNumbers(self, nums: list[int]) -> int:
        return sum(nums)

tests = [
    (
        ([1, 2, 3],),     # input tuple
        6,                # output
    ),
    (
        ([4, 5, 6, 7],),  # input tuple
        22,               # output
    ),
]
```

Now, run the code locally by doing:

```console
> pyleet add_numbers.py
Test 1 - ([1, 2, 3])......................................................PASSED
Test 2 - ([4, 5, 6, 7])...................................................PASSED
```

## Custom Validators

In some questions, you don't just have to match expected output with function output. For eg, in some questions it might ask you to modify a list in-place, or some questions might have many acceptable answers.

For that case, you can provide your own custom `validator` function.

A validator is a function that receives 3 arguments:

- `method`: your leetcode solution function
- `inputs`: your test inputs tuple
- `expected`: your expected test output value

To make assertions, you have to use `assert` statements in the following way:

```python
assert output == expected, (output, expected)  # this tuple is important!
```

For example, let's add custom validation to the `addNumbers` method:

```python
class Solution:
    def addNumbers(self, nums: list[int]) -> int:
        return sum(nums)

tests = [
    (
        ([1, 2, 3],),     # input tuple
        6,                # output
    ),
    (
        ([4, 5, 6, 7],),  # input tuple
        22,               # output
    ),
]

def validator(addNumbers, inputs, expected):
    nums = inputs[0]
    output = addNumbers(nums)
    assert output == expected, (output, expected)
```

Here's a more elaborate example, [remove_duplicates](https://leetcode.com/problems/remove-duplicates-from-sorted-array/):

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        offset = 0
        values: set[int] = set()
        for index, num in enumerate(nums):
            nums[index - offset] = num

            if num in values:
                offset += 1
            else:
                values.add(num)

        new_length = len(nums) - offset
        return new_length


tests = [
    (
        ([1, 1, 2],),
        (2, [1, 2]),
    ),
    (
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],),
        (5, [0, 1, 2, 3, 4]),
    ),
]


def validator(removeDuplicates, inputs, outputs):
    nums, = inputs
    length, expected = outputs

    new_length = removeDuplicates(nums)

    assert length == new_length, (length, new_length)
    assert nums[:new_length] == expected, (nums[:new_length], expected)
```

Run the file against sample inputs by doing:

```console
> pyleet remove_duplicates.py
Test 1 - ([1, 2, 2])......................................................PASSED
Test 2 - ([0, 1, 2, 3, 4, 2, 2, 3, 3, 4]).................................PASSED
```

### Code Snippets

If you're using VSCode, you can use the provided [code snippets](https://github.com/tusharsadhwani/python_leetcode_runner/blob/master/python.code-snippets) to help write the test cases faster.
