# -*- coding: utf-8 -*-
"""Constraints File

This file is used to define and implement the constraints used in the optimization.
"""
import math

from gurobipy import LinExpr, Model


def create_pilot_flight_assignment_constraint(model: Model, pilots, flights, pilot_flight_assignment_vars) -> None:
    for flight in flights:
        exp = LinExpr()
        for pilot in pilots:
            exp += pilot_flight_assignment_vars.data[pilot][flight].variable
        name = f'Flight_Pilot_Assignment_Const_{flight}'
        model.addConstr(exp <= LinExpr(1), name=name)

    for pilot in pilots:
        exp = LinExpr()
        for flight in flights:
            exp += pilot_flight_assignment_vars.data[pilot][flight].variable
        name = f'Pilot_Flight_Assignment_Const_{pilot}'
        model.addConstr(exp <= LinExpr(1), name=name)


def create_pilot_pairing_assignment_constraint(model: Model, pilots, pairings, pilot_pairing_assignment_vars) -> None:
    for pairing in pairings:
        exp = LinExpr()
        for pilot in pilots:
            exp += pilot_pairing_assignment_vars.data[pilot][pairing].variable
        name = f'Pilot_Pairing_Assignment_Const_{pilot}_{pairing}'
        model.addConstr(exp <= LinExpr(1), name=name)


def create_idle_pilots_constraint(model: Model, pilots, pilot_flight_assignment_vars) -> None:
    idle_pilots_number = math.floor(4 * len(pilots) / 5)

    _sum = LinExpr()
    for assignment in pilot_flight_assignment_vars.values():
        _sum += assignment.variable
    name = 'Idle_Pilots_Constraint'
    model.addConstr(_sum <= idle_pilots_number, name=name)
