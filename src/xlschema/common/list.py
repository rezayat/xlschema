"""General List class."""
from itertools import groupby


class List:
    """A utility class to hold list operating functions."""

    @staticmethod
    def unique(iterable):
        """Order preserving transformation of list with dropped duplicates.

        >>> List.unique([1, 1, 2, 3, 3, 4])
        [1, 2, 3, 4]
        """
        _list = []
        for item in iterable:
            if item not in _list:
                _list.append(item)
        return _list

    @staticmethod
    def iterate(iterable):
        """Generates a progress bar."""
        return iterable

    @staticmethod
    def enumerate(iterable):
        """Generates a progress bar with enumeration.

        >>> for i, o in List.enumerate(range(2)):
        ...    print(i, o)
        0 0
        1 1
        """
        return enumerate(iterable)

    @staticmethod
    def is_empty(iterable):
        """Returns False if no truth elements in the iterable.

        >>> List.is_empty((None, None))
        True
        """
        return not any(list(iterable))

    @staticmethod
    def isplit(iterable, sep=None):
        """Split iterable by a specified sentinel (sep).

        >>> List.isplit([1,2,3,0,4,5,6], 0)
        [[1, 2, 3], [4, 5, 6]]
        """
        return [
            list(g) for k, g in groupby(iterable, lambda x: x == sep)
            if not k
        ]

    @staticmethod
    def chunks(alist, step):
        """Split work into step sizable chunks.

        >>> List.chunks(range(20), 10)
        [range(0, 10), range(10, 20)]
        """
        return [alist[i:i + step] for i in range(0, len(alist), step)]

    @staticmethod
    def median(lst):
        """Return median value of a list of numbers.

        >>> List.median([])

        >>> List.median([1, 2, 3])
        2

        >>> List.median([1, 2, 3, 4])
        2.5
        """
        lst = sorted(lst)
        if len(lst) < 1:
            return None
        if len(lst) % 2 == 1:
            return lst[((len(lst) + 1) // 2) - 1]
        return float(sum(lst[(len(lst) // 2) - 1:(len(lst) // 2) + 1])) / 2.0
