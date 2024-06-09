# -*- coding: utf-8 -*-
"""Model Optimizer Script

This file is used to create an MILP model. The parameters, values, variables, constraints and Objective Function
are stored into the Model and optimized. After the optimization, the values of the variables are retrieved and
used to compose the Schedule solution (Dispatch Decision).
"""
from pprint import pprint
from timeit import default_timer as timer
from gurobipy import Model, GRB, LinExpr

from ProblemData import ProblemData
from milp_model.variables.variables_factory import create_flight_pilot_assignment_var, create_pairing_flight_pilot_var
from milp_model.variables.variables_factory import create_pairing_flight_var
from milp_model.variables.variables_factory import create_pairing_pilot_var

from milp_model.constraints.constraints_factory import create_idle_pilots_constraint, create_pairing_flight_constraint, \
    create_max2_constraint
from milp_model.constraints.constraints_factory import create_flight_pilot_assignment_constraint
from milp_model.constraints.constraints_factory import create_pairing_pilot_assignment_constraint
from milp_model.constraints.constraints_factory import create_max_constraint

from milp_model.solution import clean_model
from milp_model.solution import write_solution

from milp_model.visualizer import plot_flights


def set_parameters(model: Model) -> None:
    """This is used to set the parameters of the model. The parameters belong to the Gurobi Solver and are specified in
    the documentation.

    :param model: Model: The Gurobi model to be optimized.

    """
    # General parameters
    model.setParam('TimeLimit', 60 * 60)
    model.setParam('LogFile', 'output/model-gurobi.log')
    model.setParam('DisplayInterval', 1)

    # Optimization Parameters
    model.setParam('Presolve', 2)
    model.setParam('RINS', 5)
    model.setParam('Heuristics', 0.8)


def get_optimization(problem_data):
    """This function is used to create the MILP model and optimize it.
    First it creates the model, then the variables, constraints and Objective Function. And after that, it optimizes
    and writes the output and results.
    This function is used to load basic entities and some solver settings/parameters.

    :param problem_data: the input of the problem, processed in the ProblemData static class.

    """

    '''Basic Entities (lists)'''
    pilots = problem_data['pilots']
    flights = problem_data['flights']
    pairings = problem_data['pairings']
    pif_table = problem_data['pif_table']  # Pif = 1 if and only if pairing i includes flight f
    cic_table = problem_data['cic_table']  # Cif = 1 if and only if pairing i was on original schedule of crew c

    for f in flights:
        print(f, f.pilot)

    """Model Creation and Parameters"""
    model = Model('Crew Scheduling')
    model.setAttr(attrname='ModelSense', arg1=GRB.MAXIMIZE)
    set_parameters(model)

    """variables Section"""
    start = timer()
    flight_pilot_assignment_vars = create_flight_pilot_assignment_var(model=model, flights=flights, pilots=pilots)
    pairing_pilot_assignment_vars = create_pairing_pilot_var(model=model, pairings=pairings, pilots=pilots,
                                                             cic_table=cic_table)
    pairing_flight_assignment_vars = create_pairing_flight_var(model=model, pairings=pairings, flights=flights,
                                                               pif_table=pif_table)
    pairing_flight_pilot_vars = create_pairing_flight_pilot_var(model=model, pairings=pairings, pilots=pilots)
    end = timer()
    print(f'\tvariables creation time: {end - start} seconds')

    """Constraints Section"""
    start = timer()
    create_idle_pilots_constraint(model=model, pilots=pilots,
                                  pairing_pilot_assignment_vars=pairing_pilot_assignment_vars)
    # 1 to 1 constraints
    create_flight_pilot_assignment_constraint(model=model, flights=flights, pilots=pilots,
                                              flight_pilot_assignment_vars=flight_pilot_assignment_vars)
    create_pairing_pilot_assignment_constraint(model=model, pairings=pairings, pilots=pilots,
                                               pairing_pilot_assignment_vars=pairing_pilot_assignment_vars)
    create_pairing_flight_constraint(model=model, flights=flights, pairings=pairings,
                                     pairing_flight_assignment_vars=pairing_flight_assignment_vars)

    create_max_constraint(model=model, pairing_pilot_assignment_vars=pairing_pilot_assignment_vars, pairings=pairings,
                          pilots=pilots, pairing_flight_pilot_vars=pairing_flight_pilot_vars)
    create_max2_constraint(model=model, flight_pilot_assignment_vars=flight_pilot_assignment_vars, pairings=pairings,
                           pilots=pilots, pairing_flight_pilot_vars=pairing_flight_pilot_vars, flights=flights)
    end = timer()
    print(f'\tConstraints creation time: {end - start} seconds')

    '''Objective Function'''
    # of = LinExpr()
    # for pilot in pilots:
    #     for flight in flights:
    #         of += flight_pilot_assignment_vars.data[pilot][flight].variable
    # model.setObjective(of, GRB.MAXIMIZE)

    '''Optimization'''
    clean_model(model)
    model.write('output/model.lp')
    try:
        # If model is infeasible, let's find the conflicts.
        model.computeIIS()
        model.write("output/model.ilp")
    except:
        print('\tModel feasible')

        model.optimize()
        print(f'\n\n\tModel Objective Function: {model.getObjective().getValue():,.3f}')
        model.write('output/model.sol')
        model.write('output/model.mps')

        print('---PAIRINGS---')
        for pilot in pilots:
            print(f'{pilot}:')
            for pairing in pairings:
                var = pairing_pilot_assignment_vars.data[pairing][pilot]
                if var.variable.X > 0:
                    pairing.original_pilot = pilot
                    print(pairing)
            print()

        print('---FLIGHTS---')
        for flight in flights:
            print(f'{flight}: ')
            for pilot in pilots:
                var = flight_pilot_assignment_vars.data[flight][pilot]
                if var.variable.X > 0:
                    print(f'\t{pilot}', end='')
            print()

        print('---PLOT PAIRINGS---')
        for pilot in pilots:
            for pairing in pairings:
                var = pairing_pilot_assignment_vars.data[pairing][pilot]
                if var.variable.X > 0:
                    plot_flights(pairing)
            print()

        # write_solution(flight_pilot_assignment_vars, 'output/solution.xlsx')
