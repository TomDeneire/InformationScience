"""
Example of list versus generator
"""

from typing import Iterator


def my_list() -> list:
    result = []
    for number in range(0, 100):
        result.append(number)
    return result


def my_generator() -> Iterator[int]:
    for number in range(0, 100):
        yield number


for item in my_list():
    # the complete list is built before print()
    print(item, end=",")

print("\n")

for item in my_generator():
    # the generator yields one item, which is printed
    # then it yields the next, etcetera
    print(item, end=",")
