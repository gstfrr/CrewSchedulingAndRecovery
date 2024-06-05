# -*- coding: utf-8 -*-
"""variables File

This file is used to define and implement the variables used in the optimization.
"""
import itertools
from collections import defaultdict
from gurobipy import Model

from ProblemData import ProblemData, DataDictionary, Pilot
from milp_model.variables.variables import PilotFlightAssignment
from milp_model.variables.variables import PilotPairingAssignment


def create_pilot_flight_assignment_var(model: Model, pilots, flights) -> DataDictionary:
    pilot_flight_assignment_var = DataDictionary()

    pairs = itertools.product(pilots, flights)

    for pilot, flight in pairs:
        var = PilotFlightAssignment(model, pilot=pilot, flight=flight, objective=1)
        pilot_flight_assignment_var.data[pilot][flight] = var

    return pilot_flight_assignment_var


def create_pilot_pairing_assignment_var(model: Model, pilots, pairings, sic_table) -> DataDictionary:
    pilot_pairing_assignment_var = DataDictionary()

    pairs = itertools.product(pilots, pairings)

    for pilot, pairing in pairs:
        objective = 1
        if sic_table.data[pairing][pilot] == 1:
            objective = -ProblemData.PILOT_SCHEDULE_CHANGED
        var = PilotPairingAssignment(model, pilot=pilot, pairing=pairing, objective=objective)
        pilot_pairing_assignment_var.data[pilot][pairing] = var

    return pilot_pairing_assignment_var
