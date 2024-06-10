# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Any, Set, Iterable, Self


def get_leaves(struct: Iterable) -> Set[Any]:
    """This is an useful function to flatten dictionaries into a list. It is used to iterate over the values of the
     dictionary without using nested loops in the keys.

    :param struct: Iterable: DictionaryData: The structure to be flattened.

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
    """Pilot Class. """

    def __init__(self, name: str) -> None:
        self.name = name
        self.pairings = []

    def __repr__(self) -> str:
        return f"Pilot({self.name})"

    def assign_pairing(self, pairing, alert: bool = False) -> None:
        """This function will the pilot to the pairing and its flights.

        :param alert: bool: Print alert if the flight is already assigned to another pilot.
        :param pairing: Pairing to be assigned to the pilot.

        """
        self.pairings.append(pairing)
        pairing.pilot = self
        for f in pairing.flights:
            if f.pilot is not None and alert:
                print(f'\n\n\t\tFLIGHT {f.name}/{pairing.name} ALREADY ASSIGNED TO {f.pilot.name}.'
                      + f' REASSIGNING TO {self.name}.\n\n')
            f.pilot = self

    def clear_pairings(self) -> None:
        """This function remove the pilot from the pairings and their flights. """

        for p in self.pairings:
            p.pilot = None
            for f in p.flights:
                f.pilot = None
        self.pairings.clear()


class Flight:
    """FLight class. """

    def __init__(self, origin, destination, start, end) -> None:
        self.origin = origin
        self.destination = destination

        self._name = None

        if type(start) is str:
            start = datetime.strptime(start, "%Y-%m-%d %H:%M")
        if type(end) is str:
            end = datetime.strptime(end, "%Y-%m-%d %H:%M")

        self.start = start
        self.end = end
        self.pilot = None

    def __repr__(self) -> str:
        return f'{self._name}[{self.origin}->{self.destination}]'

    @property
    def name(self) -> str:
        """ """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """

        :param name: str: 

        """
        self._name = name


class Pairing:
    """Pairing Class. A  pairing is a sequence of flights (two or more) that starts and ends at the same airport
    (being crew home base)"""

    def __init__(self) -> None:
        self._name = None
        self.flights = []
        self.total_duty_time = timedelta()
        self.pilot = None

    @property
    def start(self) -> datetime:
        """Return the start of the pairing (start of first flight). """
        return min(f.start for f in self.flights)

    @property
    def end(self) -> datetime:
        """Return the end of the pairing (end of last flight). """
        return max(f.end for f in self.flights)

    @property
    def name(self) -> str:
        """ """
        return f'P{self._name}'

    @name.setter
    def name(self, name) -> None:
        """

        :param name: 

        """
        self._name = name

    def add_flight(self, flight: Flight) -> None:
        """

        :param flight: Flight: flight to be added in the pairing flights list.

        """
        if not self.flights:
            self.flights.append(flight)
            self.total_duty_time = flight.end - flight.start
        else:
            last_flight = self.flights[-1]
            layover = flight.start - last_flight.end
            self.total_duty_time += layover + (flight.end - flight.start)
            self.flights.append(flight)

    def is_legal(self, max_duty_time: timedelta) -> bool:
        """

        :param max_duty_time: timedelta: verify if the pairing has less than 10 hours of duty time.

        """
        return self.total_duty_time <= max_duty_time

    def ends_at(self, airport) -> bool:
        """

        :param airport: return the last airport in the pairing.

        """
        return self.flights[-1].destination == airport if self.flights else True

    def __repr__(self) -> str:
        pilot_name = self.pilot.name if self.pilot else '----'
        num_flights = len(self.flights)
        flights_names = ''.join(f'{f}->' for f in self.flights)
        duration = self.total_duty_time
        return f'Pairing({self.name}) {pilot_name} {num_flights} flights {flights_names} {duration}'

    @staticmethod
    def merge_pairings(pairings) -> Self:
        """This function will merge the pairings of a pilot into a single pairing. This is useful to plot the timeline.

        :param pairings: list of pairings to be merged.

        """
        if len(pairings) == 1:
            return pairings[0]

        new_name = ''
        merged_pairing = Pairing()
        for p in pairings:
            merged_pairing.pilot = p.pilot
            merged_pairing.flights.extend(p.flights)
            new_name += '+' + p.name
        merged_pairing.name = new_name

        return merged_pairing
