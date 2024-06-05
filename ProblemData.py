# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from itertools import chain, combinations, permutations
from collections import defaultdict
from typing import Any, Set, Self

days_per_week = 7


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
        return f"{self.name}"


class Flight:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __repr__(self):
        return f"{self.name}"


class Pairing:
    def __init__(self, name, flights):
        self.name = f'F({name})'
        self._flights = flights
        self.original_pilot = None

        duration = sum(x.duration for x in self.flights)
        self.start = 0
        self.end = self.start + duration

    def __repr__(self):
        return self.name

    @property
    def flights(self):
        return self._flights

    @flights.setter
    def flights(self, value):
        self._flights = value


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""
    UNASSIGNED_FLIGHT = 4
    ASSIGNING_PAIRING = 4
    UNASSIGNING_PAIRING = 4
    PILOT_SCHEDULE_CHANGED = 4

    crew = []
    flights = []
    pairings = []
    pif_table = DataDictionary()

    demands = DataDictionary()

    @staticmethod
    def basic_process(input_data):
        print()

        '''Basic Entities'''
        ProblemData.crew = [
            Pilot('John'), Pilot('Albert'), Pilot('Mary'), Pilot('Kate'),
            Pilot('Alice'), Pilot('Bob'), Pilot('David'),
            Pilot('Eve'), Pilot('Frank'), Pilot('George'),
        ]

        ProblemData.flights = [
            Flight('AZU123', 4), Flight('TAM234', 3),
            Flight('GLO345', 2), Flight('DAE456', 5.5),
            Flight('QFA567', 1),
        ]

        # # permutations of flights
        # ProblemData.pairings = list(
        #     chain(*map(lambda x: permutations(ProblemData.flights, x), range(2, len(ProblemData.flights) + 1))))

        # combinations of flights: use this for smaller cases
        pairings = list(
            chain(*map(lambda x: combinations(ProblemData.flights, x), range(2, len(ProblemData.flights) + 1))))

        for i, p in enumerate(pairings):
            pp = Pairing(i, p)
            ProblemData.pairings.append(pp)

        for pairing in ProblemData.pairings:
            for flight in ProblemData.flights:
                ProblemData.pif_table.data[pairing][flight] = 1

        # Save all our data in the dictionary below. Since ProblemData is static,
        # these values can be accessed by the class itself.
        problem_data = {'pilots': ProblemData.crew, 'flights': ProblemData.flights, 'pairings': ProblemData.pairings,
                        'pif_table': ProblemData.pif_table}

        return problem_data
