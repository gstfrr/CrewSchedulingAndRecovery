# -*- coding: utf-8 -*-
"""Model Optimizer Script

This file is used to create an MILP model. The parameters, values, variables, constraints and Objective Function
are stored into the Model and optimized. After the optimization, the values of the variables are retrieved and
used to compose the Schedule solution (Dispatch Decision).
"""
from timeit import default_timer as timer
from gurobipy import Model, GRB

from milp_model.variables.variables_factory import create_pilot_flight_assignment_var
from milp_model.variables.variables_factory import create_pilot_pairing_assignment_var

from milp_model.constraints.constraints_factory import create_pilot_flight_assignment_constraint
from milp_model.constraints.constraints_factory import create_pilot_pairing_assignment_constraint
from milp_model.constraints.constraints_factory import create_idle_pilots_constraint

from milp_model.solution import clean_model


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
    model = Model('Crew Scheduling')
    model.setAttr(attrname='ModelSense', arg1=GRB.MAXIMIZE)

    """Parameters"""
    set_parameters(model)

    '''Basic Entities (lists)'''
    pilots = problem_data['pilots']
    flights = problem_data['flights']
    pairings = problem_data['pairings']
    pif_table = problem_data['pif_table']
    sic_table = problem_data['sic_table']

    '''Dictionaries'''

    """variables Section"""
    start = timer()
    pilot_flight_assignment_vars = create_pilot_flight_assignment_var(model=model, pilots=pilots, flights=flights)
    pilot_pairing_assignment_vars = create_pilot_pairing_assignment_var(model=model, pilots=pilots, pairings=pairings,
                                                                        sic_table=sic_table)
    end = timer()
    print(f'\tvariables creation time: {end - start} seconds')

    """Constraints Section"""
    start = timer()
    create_idle_pilots_constraint(model=model, pilots=pilots, pilot_flight_assignment_vars=pilot_flight_assignment_vars)
    create_pilot_pairing_assignment_constraint(model=model, pilots=pilots, pairings=pairings,
                                               pilot_pairing_assignment_vars=pilot_pairing_assignment_vars)
    create_pilot_flight_assignment_constraint(model=model, pilots=pilots, flights=flights,
                                              pilot_flight_assignment_vars=pilot_flight_assignment_vars)
    end = timer()
    print(f'\tConstraints creation time: {end - start} seconds')

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

        '''Write Result'''
        for var in pilot_flight_assignment_vars.values():
            if var.variable.X == 1:
                print(f'\t{var.pilot} -> {var.flight}')
