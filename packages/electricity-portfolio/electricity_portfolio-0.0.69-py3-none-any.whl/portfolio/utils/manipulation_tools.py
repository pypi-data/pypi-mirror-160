from typing import Any


def element_to_end(l: list, element: Any):
    l.append(l.pop(l.index(element)))
