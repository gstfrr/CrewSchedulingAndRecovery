# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
import math
from datetime import datetime
from pprint import pprint

from Domain import DataDictionary, Flight, Pilot
from pairing_generator import generate_pairings

days_per_week = 7


def create_pilots():
    ProblemData.crew = [
        Pilot('Alice'), Pilot('Bob'), Pilot('David'),
        Pilot('Eve'), Pilot('Frank'), Pilot('George'),
        Pilot('John'), Pilot('Albert'), Pilot('Mary'), Pilot('Kate'),
        Pilot('Carl'), Pilot('Julio'), Pilot('Joanne'), Pilot('Sandra'),
    ]
    ProblemData.crew.sort(key=lambda x: x.name)


def create_flights():
    ProblemData.flights = [
        Flight("JFK", "LAX", "08:15", "10:00"),
        Flight("JFK", "ODR", "08:30", "09:00"),
        Flight("LAX", "ODR", "11:00", "13:00"),
        Flight("VOV", "JFK", "07:00", "10:15"),
        Flight("WAR", "VOV", "08:30", "09:30"),
        Flight("LAX", "VOV", "11:00", "17:00"),
        Flight("ODR", "DFW", "06:00", "15:30"),
        Flight("DFW", "JFK", "17:00", "20:30"),
        Flight("ODR", "WAR", "11:00", "14:45"),
        Flight("WAR", "DFW", "13:30", "17:30"),
        Flight("WAR", "JFK", "17:00", "20:30")
    ]
    ProblemData.flights.sort(key=lambda x: x.origin)
    for i, f in enumerate(ProblemData.flights):
        f.name = i


def create_pif_table():
    for pairing in ProblemData.pairings:
        for flight in ProblemData.flights:
            if flight in pairing.flights:
                ProblemData.pif_table.data[pairing][flight] = 1
            else:
                ProblemData.pif_table.data[pairing][flight] = 0


def create_cic_table():
    for pairing in ProblemData.pairings:
        for pilot in ProblemData.crew:
            if pairing.original_pilot == pilot:
                ProblemData.cic_table.data[pairing][pilot] = 1
            else:
                ProblemData.cic_table.data[pairing][pilot] = 0


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""
    UNASSIGNED_FLIGHT = 1
    ASSIGNING_PAIRING = 1
    UNASSIGNING_PAIRING = 1
    PILOT_SCHEDULE_CHANGED = 1

    BACKUP_PILOTS_PERCENT = .2

    INITIAL_DATE = datetime(2024, 1, 1)

    crew = []
    flights = []
    pairings = []
    pif_table = DataDictionary()
    cic_table = DataDictionary()

    @staticmethod
    def basic_process(input_data):
        print()

        '''Basic Entities'''
        # C - set of crew (pilots)
        create_pilots()
        # F - set of non-cancelled flights
        create_flights()
        # P - set of pairings generated from flights F
        ProblemData.pairings = generate_pairings(ProblemData.flights)

        '''Assigning Pilots to Pairings/Flights'''
        ProblemData.crew[0].assign_pairing(ProblemData.pairings[16])
        ProblemData.crew[1].assign_pairing(ProblemData.pairings[5])  # 23
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
        # Cif = 1 if and only if pairing i was on original schedule of crew c
        create_cic_table()

        print('\n', '-' * 10, 'STATS', '-' * 10)
        print('\tNumber of flights: ', len(ProblemData.flights))
        print('\tNumber of pairings: ', len(ProblemData.pairings))
        print('\tNumber of pilots: ', len(ProblemData.crew))
        print('\tNumber of idle pilots: ', math.ceil(len(ProblemData.crew) * ProblemData.BACKUP_PILOTS_PERCENT))

        print('\n', '-' * 10, 'FLIGHTS', '-' * 10)
        for f in ProblemData.flights:
            print('\t', f)

        print('\n', '-' * 10, 'PAIRINGS', '-' * 10)
        for p in ProblemData.pairings:
            print(p)

        # Save all our data in the dictionary below. Since ProblemData is static,
        # these values can be accessed by the class itself.
        problem_data = {'pilots': ProblemData.crew, 'flights': ProblemData.flights, 'pairings': ProblemData.pairings,
                        'pif_table': ProblemData.pif_table, 'cic_table': ProblemData.cic_table, }

        return problem_data
