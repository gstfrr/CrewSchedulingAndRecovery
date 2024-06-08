# -*- coding: utf-8 -*-
"""Problem Data

This file is used to define all the domain classes for basic and complex entities that will be used in the optimization.
The entities are defined as classes and the data is stored in dictionaries for O(1) time access and manipulation.
"""
from datetime import datetime

from Domain import DataDictionary, Flight, Pilot
from pairing_generator import generate_pairings

days_per_week = 7


class ProblemData:
    """This class is used to store all the data of the problem. It is a static class, so it can be accessed anywhere"""
    UNASSIGNED_FLIGHT = 2.2
    ASSIGNING_PAIRING = 3.3
    UNASSIGNING_PAIRING = 4.4
    PILOT_SCHEDULE_CHANGED = 5.5

    BACKUP_PILOTS_PERCENT = .1

    INITIAL_DATE = datetime(2024, 1, 1)

    crew = []
    flights = []
    pairings = []
    pif_table = DataDictionary()
    cic_table = DataDictionary()

    demands = DataDictionary()

    @staticmethod
    def basic_process(input_data):
        print()

        '''Basic Entities'''
        ProblemData.crew = [
            Pilot('John'), Pilot('Albert'), Pilot('Mary'), Pilot('Kate'),
            Pilot('Alice'), Pilot('Bob'), Pilot('David'),
            # Pilot('Eve'), Pilot('Frank'), Pilot('George'),
        ]
        ProblemData.crew.sort(key=lambda x: x.name)

        ProblemData.flights = [
            Flight(1, "JFK", "LAX", "08:00", "10:00"),
            Flight(2, "LAX", "ORD", "11:00", "13:00"),
            Flight(3, "ORD", "DFW", "14:00", "16:00"),
            Flight(4, "DFW", "JFK", "17:00", "19:00")
        ]

        # permutations of flights
        ProblemData.pairings = generate_pairings(ProblemData.flights)

        for pairing in ProblemData.pairings:
            for flight in ProblemData.flights:
                if flight in pairing.flights:
                    ProblemData.pif_table.data[pairing][flight] = 1
                else:
                    ProblemData.pif_table.data[pairing][flight] = 0

        # John Albert Mary Kate
        ProblemData.crew[0].assign_pairing(ProblemData.pairings[37])
        ProblemData.crew[1].assign_pairing(ProblemData.pairings[11])
        ProblemData.crew[2].assign_pairing(ProblemData.pairings[20])
        ProblemData.crew[3].assign_pairing(ProblemData.pairings[9])
        ProblemData.crew[4].assign_pairing(ProblemData.pairings[24])
        ProblemData.crew[5].assign_pairing(ProblemData.pairings[1])
        ProblemData.crew[6].assign_pairing(ProblemData.pairings[33])
        # ProblemData.crew[7].assign_pairing(ProblemData.pairings[13])
        # ProblemData.crew[8].assign_pairing(ProblemData.pairings[22])
        # ProblemData.crew[9].assign_pairing(ProblemData.pairings[25])

        for pairing in ProblemData.pairings:
            for pilot in ProblemData.crew:
                if pairing.original_pilot == pilot:
                    ProblemData.cic_table.data[pairing][pilot] = 1
                else:
                    ProblemData.cic_table.data[pairing][pilot] = 0

        # Save all our data in the dictionary below. Since ProblemData is static,
        # these values can be accessed by the class itself.
        problem_data = {'pilots': ProblemData.crew, 'flights': ProblemData.flights, 'pairings': ProblemData.pairings,
                        'pif_table': ProblemData.pif_table, 'cic_table': ProblemData.cic_table, }

        return problem_data
