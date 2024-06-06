# -*- coding: utf-8 -*-
"""variables File

This file is used to define and implement the variables used in the optimization.
"""
import itertools
from collections import defaultdict
from gurobipy import Model

from ProblemData import ProblemData, DataDictionary, Pilot
from milp_model.variables.variables import FlightPilotAssignmentVar
from milp_model.variables.variables import PilotPairingAssignmentVar
from milp_model.variables.variables import StartTimeVar
from milp_model.variables.variables import PrecedenceVar


def create_flight_pilot_assignment_var(model: Model, pilots, flights) -> DataDictionary:
    flight_pilot_assignment_vars = DataDictionary()

    pairs = itertools.product(pilots, flights)

    for pilot, flight in pairs:
        var = FlightPilotAssignmentVar(model, pilot=pilot, flight=flight, objective=1)
        flight_pilot_assignment_vars.data[pilot][flight] = var

    return flight_pilot_assignment_vars


def create_precedence_var(model: Model, pilots, flights) -> DataDictionary:
    precedence_vars = DataDictionary()

    for pilot, flight1, flight2 in itertools.product(pilots, flights, flights):
        if flight1 != flight2:
            var = PrecedenceVar(model, pilot=pilot, flight1=flight1, flight2=flight2)
            precedence_vars.data[pilot][flight1][flight2] = var

    return precedence_vars


def create_start_time_var(model: Model, pilots, flights) -> DataDictionary:
    star_time_vars = DataDictionary()

    pairs = itertools.product(pilots, flights)

    for pilot, flight in pairs:
        var = StartTimeVar(model, pilot=pilot, flight=flight)
        star_time_vars.data[pilot][flight] = var

    return star_time_vars


def create_pilot_pairing_assignment_var(model: Model, pilots, pairings, sic_table) -> DataDictionary:
    pilot_pairing_assignment_vars = DataDictionary()

    pairs = itertools.product(pilots, pairings)

    for pilot, pairing in pairs:
        objective = 1
        if sic_table.data[pairing][pilot] == 0:
            objective = -ProblemData.PILOT_SCHEDULE_CHANGED
        var = PilotPairingAssignmentVar(model, pilot=pilot, pairing=pairing, objective=objective)
        pilot_pairing_assignment_vars.data[pilot][pairing] = var

    return pilot_pairing_assignment_vars
