# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Any, Set, Iterable


def get_leaves(struct: Iterable) -> Set[Any]:
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


def rec_dd() -> defaultdict:
    """Useful function to create a recursive dictionary. This is useful to avoid key errors when accessing."""
    return defaultdict(rec_dd)


class DataDictionary:
    """All the dictionaries in the project are stores in this class. It provides the values() method that
    returns a flatten list of the dictionary. The flatten list can be used to direct iteration
    instead of using nested loops.

    """

    def __init__(self) -> None:
        self.data = rec_dd()  # data is still visible for O(1) access

    def values(self) -> Set[Any]:
        """ """
        return get_leaves(self.data)  # Flattening available to avoid huge nested loops


class Pilot:
    def __init__(self, name: str) -> None:
        self.name = name
        self.original_pairing = None

    def __repr__(self) -> str:
        return f"Pilot({self.name})"

    def assign_pairing(self, pairing) -> None:
        self.original_pairing = pairing
        pairing.original_pilot = self
        for f in pairing.flights:
            f.pilot = self


class Flight:
    def __init__(self, origin, destination, start, end) -> None:
        self.origin = origin
        self.destination = destination

        self._name = None

        self.start = start
        self.end = end
        self.pilot = None

    def __repr__(self) -> str:
        return f'{self._name}[{self.origin}->{self.destination}]'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name


class Pairing:
    def __init__(self) -> None:
        self._name = None
        self.flights = []
        self.total_duty_time = timedelta()
        self.original_pilot = None

    @property
    def start(self) -> datetime:
        return min(f.start for f in self.flights)

    @property
    def end(self) -> datetime:
        return max(f.end for f in self.flights)

    @property
    def name(self) -> str:
        return f'P{self._name}'

    @name.setter
    def name(self, name) -> None:
        self._name = name

    def add_flight(self, flight: Flight) -> None:
        if not self.flights:
            self.flights.append(flight)
            self.total_duty_time = flight.end - flight.start
        else:
            last_flight = self.flights[-1]
            layover = flight.start - last_flight.end
            self.total_duty_time += layover + (flight.end - flight.start)
            self.flights.append(flight)

    def is_legal(self, max_duty_time: timedelta) -> bool:
        return self.total_duty_time <= max_duty_time

    def ends_at(self, airport) -> bool:
        return self.flights[-1].destination == airport if self.flights else True

    def __repr__(self) -> str:
        pilot_name = self.original_pilot.name if self.original_pilot else '----'
        return (f'Pairing({self.name}) - {pilot_name} - {len(self.flights)} - ' +
                ''.join(f'{f}->' for f in self.flights) + f' - {self.total_duty_time}')
