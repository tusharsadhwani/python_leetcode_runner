from dataclasses import dataclass
from typing import Optional, Union


class Solution:
    def dummy(*_: object) -> None: ...


@dataclass
class ListNode:
    value: int
    next: Optional['ListNode']

    def print(self) -> None:
        current = self
        while current.next is not None:
            print(current.value, end=', ')
            current = current.next

        print(current.value)


class MyLinkedList:
    def __init__(self) -> None:
        self.head: Optional[ListNode] = None
        self.tail: Optional[ListNode] = None

    def get(self, index: int) -> int:
        current_index = 0
        current_node = self.head
        while current_node is not None:
            if current_index == index:
                return current_node.value

            current_index += 1
            current_node = current_node.next

        return -1

    def addAtHead(self, val: int) -> None:
        if self.head is None or self.tail is None:
            self.head = self.tail = ListNode(value=val, next=None)
            return

        new_head = ListNode(value=val, next=self.head)
        self.head = new_head

    def addAtTail(self, val: int) -> None:
        if self.head is None or self.tail is None:
            self.head = self.tail = ListNode(value=val, next=None)
            return

        new_tail = ListNode(value=val, next=None)
        self.tail.next = new_tail
        self.tail = new_tail

    def addAtIndex(self, index: int, val: int) -> None:
        current_index = 0
        prev_node: Optional[ListNode] = None
        current_node = self.head

        while current_node is not None:
            if current_index == index:
                if prev_node is not None:
                    new_node = ListNode(value=val, next=current_node)
                    prev_node.next = new_node
                else:
                    self.addAtHead(val)

                return

            prev_node = current_node
            current_node = current_node.next
            current_index += 1

        # Edge case: appending
        if current_index == index:
            self.addAtTail(val)

    def deleteAtIndex(self, index: int) -> None:
        current_index = 0
        prev_node: Optional[ListNode] = None
        current_node = self.head

        while current_node is not None:
            if current_index == index:
                if prev_node is None:
                    self.head = current_node.next
                else:
                    prev_node.next = current_node.next

                # Edge case: deleted last node
                if current_node.next is None:
                    self.tail = prev_node

                return

            prev_node = current_node
            current_node = current_node.next
            current_index += 1


tests = [
    (
        (["addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"],
         [[1], [3], [1, 2], [1], [1], [1]],),
        [None, None, None, 2, None, 3],
    ),
    (
        (["addAtHead", "addAtHead", "addAtHead", "addAtIndex", "deleteAtIndex", "addAtHead", "addAtTail", "get", "addAtHead", "addAtIndex", "addAtHead"],
         [[7], [2], [1], [3, 0], [2], [6], [4], [4], [4], [5, 0], [6]],),
        [None, None, None, None, None, None, None, 4, None, None, None],
    ),
    (
        (["addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"],
         [[1], [3], [1, 2], [1], [0], [0]],),
        [None, None, None, 2, None, 2],
    ),
    (
        (["addAtIndex", "addAtIndex", "addAtIndex", "get"],
         [[0, 10], [0, 20], [1, 30], [0]],),
        [None, None, None, 20],
    ),
]


def validator(
        _: object,
        inputs: tuple[list[str], list[list[int]]],
        expected: list[Union[bool, int, None]]
) -> None:
    obj = MyLinkedList()
    method = zip(*inputs)
    for (method_name, args), expected_val in zip(method, expected):
        retval = getattr(obj, method_name)(*args)
        assert retval == expected_val, (retval, expected_val)
