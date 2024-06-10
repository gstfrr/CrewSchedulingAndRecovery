# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
import math

from Domain import DataDictionary, Flight, Pilot, Pairing
from pairing_generator import generate_pairings


def create_pilots(input_pilots: list[dict]) -> None:
    """

    :param input_pilots: list[dict]: 

    """
    for p in input_pilots:
        pilot = Pilot(name=p['name'])
        ProblemData.crew.append(pilot)

    ProblemData.crew.sort(key=lambda x: x.name)


def create_flights(input_flights: list[dict]) -> None:
    """

    :param input_flights: list[dict]: 

    """
    for f in input_flights:
        flight = Flight(origin=f['origin'], destination=f['destination'], start=f['start'], end=f['end'])
        ProblemData.flights.append(flight)

    ProblemData.flights.sort(key=lambda x: x.origin)
    for i, f in enumerate(ProblemData.flights):
        f.name = i


def create_pif_table() -> None:
    """Creates a dictionary containing binary values.
    Pif = 1 if and only if pairing i includes flight f."""
    for pairing in ProblemData.pairings:
        for flight in ProblemData.flights:
            if flight in pairing.flights:
                ProblemData.pif_table.data[pairing][flight] = 1
            else:
                ProblemData.pif_table.data[pairing][flight] = 0


def create_cic_table() -> None:
    """Creates a dictionary containing binary values.
    Cic = 1 if and only if pairing i was on original schedule of crew c."""
    for pairing in ProblemData.pairings:
        for pilot in ProblemData.crew:
            if pairing.original_pilot == pilot:
                ProblemData.cic_table.data[pairing][pilot] = 1
            else:
                ProblemData.cic_table.data[pairing][pilot] = 0


def set_parameters(input_parameters: list[dict]) -> None:
    """This function is used to set the parameters of the problem. It will assign values to the ProblemData constants.

    :param input_parameters: list[dict]: list of parameters string and value.

    """
    for p in input_parameters:
        setattr(ProblemData, p['name'], p['value'])


def print_stats() -> None:
    """Print the statistics of the problem. It will print the number of flights, pairings, pilots and idle pilots. It
    is useful in the beginning of the optimization to check if the data was loaded correctly.

    """
    print('\n', '-' * 10, 'STATS', '-' * 10)
    print('\tNumber of flights: ', len(ProblemData.flights))
    print('\tNumber of pairings: ', len(ProblemData.pairings))
    print('\tNumber of pilots: ', len(ProblemData.crew))
    print('\tNumber of idle pilots: ', math.ceil(len(ProblemData.crew) * ProblemData.BACKUP_PILOTS_PERCENT))

    print('\n', '-' * 10, 'FLIGHTS', '-' * 10)
    for f in ProblemData.flights:
        print('\t', f, f.pilot.name if f.pilot else '----')

    print('\n', '-' * 10, 'PAIRINGS', '-' * 10)
    for p in ProblemData.pairings:
        print(p)


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""
    INITIAL_DATE = None
    BACKUP_PILOTS_PERCENT = None

    UNASSIGNED_FLIGHT = None
    ASSIGNING_PAIRING = None
    UNASSIGNING_PAIRING = None
    PILOT_SCHEDULE_CHANGED = None

    crew = []
    flights = []
    pairings = []
    pif_table = DataDictionary()
    cic_table = DataDictionary()

    @staticmethod
    def basic_process(input_data: dict) -> dict[str, DataDictionary | list | list[Pairing]]:
        """This function is used to load basic entities and some solver settings/parameters. Here is where the entities
        are constructed and the data is stored in the ProblemData class.

        :param input_data: dict: 

        """
        '''Basic Entities'''
        set_parameters(input_data['Parameters'])

        # C - set of crew (pilots)
        create_pilots(input_data['Crew'])

        # F - set of non-cancelled flights
        create_flights(input_data['Flights'])

        # P - set of pairings generated from flights F
        ProblemData.pairings = generate_pairings(ProblemData.flights)

        '''Assigning Pilots to Pairings/Flights'''
        ProblemData.crew[0].assign_pairing(ProblemData.pairings[38])
        ProblemData.crew[1].assign_pairing(ProblemData.pairings[4])  # 23
        ProblemData.crew[2].assign_pairing(ProblemData.pairings[17])
        # ProblemData.crew[3].assign_pairing(ProblemData.pairings[9])
        # ProblemData.crew[4].assign_pairing(ProblemData.pairings[24])
        # ProblemData.crew[5].assign_pairing(ProblemData.pairings[1])
        # ProblemData.crew[6].assign_pairing(ProblemData.pairings[33])
        # ProblemData.crew[7].assign_pairing(ProblemData.pairings[13])
        # ProblemData.crew[8].assign_pairing(ProblemData.pairings[22])
        # ProblemData.crew[9].assign_pairing(ProblemData.pairings[25])

        # Pif = 1 if and only if pairing i includes flight f
        create_pif_table()
        # Cic = 1 if and only if pairing i was on original schedule of crew c
        create_cic_table()

        print_stats()

        # Save all our data in the dictionary below. Since ProblemData is static,
        # these values can be accessed by the class itself.
        problem_data = {'pilots': ProblemData.crew, 'flights': ProblemData.flights, 'pairings': ProblemData.pairings,
                        'pif_table': ProblemData.pif_table, 'cic_table': ProblemData.cic_table, }

        return problem_data
