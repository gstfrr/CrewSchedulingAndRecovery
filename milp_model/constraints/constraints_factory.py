# -*- coding: utf-8 -*-
"""Constraints File

This file is used to define and implement the constraints used in the optimization.
"""
import math

from gurobipy import LinExpr, Model


def create_idle_pilots_constraint(model: Model, pilots, flight_pilot_assignment_vars) -> None:
    idle_pilots_number = math.floor(4 * len(pilots) / 5)

    _sum = LinExpr()
    for assignment in flight_pilot_assignment_vars.values():
        _sum += assignment.variable
    name = 'Idle_Pilots_Constraint'
    model.addConstr(_sum <= idle_pilots_number, name=name)


def create_flight_pilot_assignment_constraint(model: Model, pilots, flights, flight_pilot_assignment_vars) -> None:
    for flight in flights:
        exp = LinExpr()
        for pilot in pilots:
            exp += flight_pilot_assignment_vars.data[pilot][flight].variable
        name = f'Flight_Pilot_Assignment_Const_{flight}'
        model.addConstr(exp <= LinExpr(1), name=name)


def create_precedence_integrity_constraint(model: Model, pilots, flights, precedence_vars) -> None:
    for pilot in pilots:
        for flight1 in flights:
            for flight2 in flights:
                if flight1 != flight2:
                    model.addConstr(precedence_vars.data[pilot][flight1][flight2].variable +
                                    precedence_vars.data[pilot][flight2][flight1].variable == 1,
                                    name=f'PrecedenceIntegrity_({pilot})_({flight1})_({flight2})')


def create_precedence_constraint(model: Model, start_time_vars, precedence_vars, flights, pilots) -> None:
    big_m = sum([x.duration for x in flights])

    for pilot in pilots:
        for flight1 in flights:
            for flight2 in flights:
                if flight1 != flight2:
                    lhs1 = start_time_vars.data[pilot][flight1].variable + flight1.duration - start_time_vars.data[pilot][flight2].variable
                    rhs1 = big_m * precedence_vars.data[pilot][flight1][flight2].variable
                    model.addConstr(lhs1 <= rhs1, name=f'PrecedenceBigM_({pilot})_({flight1})_({flight2})')

                    lhs2 = start_time_vars.data[pilot][flight2].variable + flight2.duration - start_time_vars.data[pilot][flight1].variable
                    rhs2 = big_m * (1 - precedence_vars.data[pilot][flight1][flight2].variable)
                    model.addConstr(lhs2 <= rhs2, name=f'PrecedenceBigM-1_({pilot})_({flight1})_({flight2})')


    # for m in precedence_vars.keys():
    #     for w1 in precedence_vars[m].keys():
    #         for w2 in precedence_vars[m][w1].keys():
    #             lhs1 = start_time_vars[m][w1] + duration[m][w1] - start_time_vars[m][w2]
    #             rhs1 = big_m * precedence_vars[m][w1][w2]
    #             model.addConstr(lhs1 <= rhs1, name=f'PrecedenceBigM_M({m.name})_-_W1({w1.name})-_W2({w2.name})')
    #
    #             lhs2 = start_time_vars[m][w2] + duration[m][w2] - start_time_vars[m][w1]
    #             rhs2 = big_m * (1 - precedence_vars[m][w1][w2])
    #             model.addConstr(lhs2 <= rhs2, name=f'PrecedenceBigM-1_M({m.name})_-_W1({w1.name})-_W2({w2.name})')
