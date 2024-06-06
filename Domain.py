# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Any, Set, Self



def get_leaves(struct) -> Set[Any]:
    """This is an useful function to flatten dictionaries into a list. It is used to iterate over the values of the
     dictionary without using nested loops in the keys.

    :param struct: DictionaryData: The structure to be flattened.

    """
    # Ref: https://stackoverflow.com/a/59832362/
    values = set()
    if isinstance(struct, dict):
        for sub_struct in struct.values():
            values.update(get_leaves(sub_struct))
    elif isinstance(struct, list):
        for sub_struct in struct:
            values.update(get_leaves(sub_struct))
    elif struct is not None:
        values.add(struct)
    return values


def rec_dd():
    """Useful function to create a recursive dictionary. This is useful to avoid key errors when accessing."""
    return defaultdict(rec_dd)


class DataDictionary:
    """All the dictionaries in the project are stores in this class. It provides the values() method that
    returns a flatten list of the dictionary. The flatten list can be used to direct iteration
    instead of using nested loops.

    """

    def __init__(self):
        self.data = rec_dd()  # data is still visible for O(1) access

    def values(self) -> Set[Any]:
        """ """
        return get_leaves(self.data)  # Flattening available to avoid huge nested loops


class Pilot:
    def __init__(self, name):
        self.name = name
        self.original_pairing = None

    def __repr__(self):
        return f"Pilot({self.name})"

    def assign_pairing(self, pairing):
        self.original_pairing = pairing
        pairing.original_pilot = self


class Flight:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

        self._start = None
        self._end = None

    def __repr__(self):
        return f"Flight({self.name})"

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._start + timedelta(hours=self.duration)


class Pairing:
    def __init__(self, name, flights=None):
        self.name = name
        self._flights = flights
        self.original_pilot = None

        duration = sum(x.duration for x in self.flights)
        self.start = 0
        self.end = self.start + duration

    def __repr__(self):
        return f'Pairing({self.name})'

    @property
    def flights(self):
        return self._flights

    @flights.setter
    def flights(self, value):
        self._flights = value
