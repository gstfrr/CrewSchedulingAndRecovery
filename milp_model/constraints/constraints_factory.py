# -*- coding: utf-8 -*-
"""Constraints File

This file is used to define and implement the constraints used in the optimization.
"""
import math

from gurobipy import LinExpr, Model

from ProblemData import ProblemData, DataDictionary
from Domain import Flight, Pairing, Pilot


def create_idle_pilots_constraint(model: Model, pilots: list[Pilot],
                                  pairing_pilot_assignment_vars: DataDictionary) -> None:
    # '''Guarantees x% of the pilots are idle.'''
    max_working_pilots = math.floor((1 - ProblemData.BACKUP_PILOTS_PERCENT) * len(pilots))

    _sum = LinExpr()
    for assignment in pairing_pilot_assignment_vars.values():
        _sum += assignment.variable
    name = 'Idle_Pilots_Constraint'
    model.addConstr(_sum <= max_working_pilots, name=name)


def create_flight_pilot_assignment_constraint(model: Model, pilots, flights, flight_pilot_assignment_vars) -> None:
    for flight in flights:
        lhs = LinExpr()
        for pilot in pilots:
            lhs += flight_pilot_assignment_vars.data[flight][pilot].variable
        name = f'Flight_Pilot_Assignment_Const_{flight}'
        model.addConstr(lhs <= LinExpr(1), name=name)


def create_pairing_pilot_assignment_constraint(model: Model, pilots: list[Pilot], pairings: list[Pairing],
                                               pairing_pilot_assignment_vars: DataDictionary) -> None:
    # '''Guarantees 1 pilot per pairing and 1 pairing per pilot'''

    for pairing in pairings:
        lhs = LinExpr()
        for pilot in pilots:
            lhs += pairing_pilot_assignment_vars.data[pairing][pilot].variable
        name = f'Pilot_Pairing_Assignment_Const_{pairing.name}'
        model.addConstr(lhs <= LinExpr(1), name=name)

    for pilot in pilots:
        lhs = LinExpr()
        for pairing in pairings:
            lhs += pairing_pilot_assignment_vars.data[pairing][pilot].variable
        name = f'Pairing_Pilot_Assignment_Const_{pilot}'
        model.addConstr(lhs <= LinExpr(1), name=name)


def create_pairing_flight_constraint(model: Model, flights: list[Flight], pairings: list[Pairing],
                                     pairing_flight_assignment_vars: DataDictionary) -> None:
    # '''Guarantees that the pairing will have all of its flights assigned.'''
    for pairing in pairings:
        lhs = LinExpr()
        rhs = len(pairing.flights)

        for flight in flights:
            if flight in pairing.flights:
                lhs += pairing_flight_assignment_vars.data[pairing][flight].variable

        name = f'Pairing_Flight_Const_{pairing.name}'
        model.addConstr(lhs == rhs, name=name)


def create_max_constraint(model: Model, pilots: list[Pilot], pairings: list[Pairing],
                          pairing_pilot_assignment_vars: DataDictionary,
                          pairing_flight_pilot_vars: DataDictionary) -> None:
    for pilot in pilots:
        for pairing in pairings:
            lhs = LinExpr()
            for flight in pairing.flights:
                lhs += pairing_flight_pilot_vars.data[pairing][flight][pilot].variable

            pairing_pilot_var = pairing_pilot_assignment_vars.data[pairing][pilot].variable
            name = f'Max_Constraint_{pilot}_{pairing.name}'
            model.addConstr(lhs == pairing_pilot_var * len(pairing.flights), name=name)


def create_max2_constraint(model: Model, pilots: list[Pilot], flights: list[Flight], pairings: list[Pairing],
                           flight_pilot_assignment_vars: DataDictionary,
                           pairing_flight_pilot_vars: DataDictionary) -> None:
    for pilot in pilots:
        for flight in flights:
            lhs = LinExpr()
            for pairing in pairings:
                if flight in pairing.flights:
                    lhs += pairing_flight_pilot_vars.data[pairing][flight][pilot].variable

            flight_pilot_var = flight_pilot_assignment_vars.data[flight][pilot].variable
            name = f'Max2_Constraint_{pilot}_{flight}'
            model.addConstr(lhs == flight_pilot_var, name=name)
