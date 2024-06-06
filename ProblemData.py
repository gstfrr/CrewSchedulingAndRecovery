# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from datetime import datetime, timedelta
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
        return f"Pilot({self.name})"

    def assign_pairing(self, pairing):
        self.original_pairing = pairing
        pairing.original_pilot = self


class Flight:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

        self._start = ProblemData.INITIAL_DATE
        self._end = self.start + timedelta(hours=self.duration)

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

    @end.setter
    def end(self, value):
        self._end = value


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


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""
    UNASSIGNED_FLIGHT = 4
    ASSIGNING_PAIRING = 4
    UNASSIGNING_PAIRING = 4
    PILOT_SCHEDULE_CHANGED = 4

    INITIAL_DATE = datetime(2024, 1, 1)

    crew = []
    flights = []
    pairings = []
    pif_table = DataDictionary()
    sic_table = DataDictionary()

    demands = DataDictionary()

    @staticmethod
    def basic_process(input_data):
        print()

        '''Basic Entities'''
        ProblemData.crew = [
            Pilot('John'), Pilot('Albert'), Pilot('Mary'), Pilot('Kate'),
            Pilot('Alice'), Pilot('Bob'),
            # Pilot('David'),
            # Pilot('Eve'), Pilot('Frank'), Pilot('George'),
        ]
        ProblemData.crew.sort(key=lambda x: x.name)

        ProblemData.flights = [
            Flight('AZU123', 4), Flight('TAM123', 3), Flight('GLO123', 2),
            Flight('DAE123', 2.5), Flight('QFA123', 1),
            # Flight('AZU234', .5),
            # Flight('TAM234', 4), Flight('GLO234', 3.5),
            # Flight('DAE234', 5.5), Flight('QFA234', 6),
        ]

        # # permutations of flights
        # pairings = list(
        #     chain(*map(lambda x: permutations(ProblemData.flights, x), range(2, len(ProblemData.flights) + 1))))

        # combinations of flights: use this for smaller cases
        pairings = list(
            chain(*map(lambda x: combinations(ProblemData.flights, x), range(2, len(ProblemData.flights) + 1))))

        for i, p in enumerate(pairings):
            pp = Pairing(i, p)
            ProblemData.pairings.append(pp)

        for pairing in ProblemData.pairings:
            for flight in ProblemData.flights:
                if flight in pairing.flights:
                    ProblemData.pif_table.data[pairing][flight] = 1
                else:
                    ProblemData.pif_table.data[pairing][flight] = 0

        ProblemData.crew[0].assign_pairing(ProblemData.pairings[22])
        ProblemData.crew[1].assign_pairing(ProblemData.pairings[11])
        ProblemData.crew[2].assign_pairing(ProblemData.pairings[20])
        ProblemData.crew[3].assign_pairing(ProblemData.pairings[9])
        ProblemData.crew[4].assign_pairing(ProblemData.pairings[17])
        ProblemData.crew[5].assign_pairing(ProblemData.pairings[15])
        # ProblemData.crew[6].assign_pairing(ProblemData.pairings[0])
        # ProblemData.crew[7].assign_pairing(ProblemData.pairings[13])
        # ProblemData.crew[8].assign_pairing(ProblemData.pairings[3])
        # ProblemData.crew[9].assign_pairing(ProblemData.pairings[25])

        for pairing in ProblemData.pairings:
            for pilot in ProblemData.crew:
                if pairing.original_pilot == pilot:
                    ProblemData.sic_table.data[pairing][pilot] = 1
                else:
                    ProblemData.sic_table.data[pairing][pilot] = 0

        # Save all our data in the dictionary below. Since ProblemData is static,
        # these values can be accessed by the class itself.
        problem_data = {'pilots': ProblemData.crew, 'flights': ProblemData.flights, 'pairings': ProblemData.pairings,
                        'pif_table': ProblemData.pif_table, 'sic_table': ProblemData.sic_table, }

        return problem_data
