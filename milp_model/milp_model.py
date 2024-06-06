# -*- coding: utf-8 -*-
"""Model Optimizer Script

This file is used to create an MILP model. The parameters, values, variables, constraints and Objective Function
are stored into the Model and optimized. After the optimization, the values of the variables are retrieved and
used to compose the Schedule solution (Dispatch Decision).
"""
from timeit import default_timer as timer
from gurobipy import Model, GRB

from ProblemData import ProblemData
from milp_model.variables.variables_factory import create_flight_pilot_assignment_var
from milp_model.variables.variables_factory import create_pilot_pairing_assignment_var
from milp_model.variables.variables_factory import create_start_time_var
from milp_model.variables.variables_factory import create_precedence_var

from milp_model.constraints.constraints_factory import create_flight_pilot_assignment_constraint
# from milp_model.constraints.constraints_factory import create_pilot_pairing_assignment_constraint
from milp_model.constraints.constraints_factory import create_idle_pilots_constraint
from milp_model.constraints.constraints_factory import create_precedence_constraint
from milp_model.constraints.constraints_factory import create_precedence_integrity_constraint

from milp_model.solution import clean_model
from milp_model.solution import write_solution

from milp_model.visualizer import visualize


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
    flight_pilot_assignment_vars = create_flight_pilot_assignment_var(model=model, flights=flights, pilots=pilots)
    # pilot_pairing_assignment_vars = create_pilot_pairing_assignment_var(model=model, pilots=pilots, pairings=pairings,
    #                                                                     sic_table=sic_table)

    start_time_vars = create_start_time_var(model, flights=flights, pilots=pilots)
    precedence_vars = create_precedence_var(model, flights=flights, pilots=pilots)
    end = timer()
    print(f'\tvariables creation time: {end - start} seconds')

    """Constraints Section"""
    start = timer()
    # create_idle_pilots_constraint(model=model, pilots=pilots, flight_pilot_assignment_vars=flight_pilot_assignment_vars)
    create_flight_pilot_assignment_constraint(model=model, flights=flights, pilots=pilots, flight_pilot_assignment_vars=flight_pilot_assignment_vars)
    # create_pilot_pairing_assignment_constraint(model=model, pilots=pilots, pairings=pairings, pilot_pairing_assignment_vars=pilot_pairing_assignment_vars)

    create_precedence_integrity_constraint(model, pilots=pilots, flights=flights, precedence_vars=precedence_vars)
    create_precedence_constraint(model, start_time_vars=start_time_vars, precedence_vars=precedence_vars, pilots=pilots, flights=flights)

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

        for pilot in pilots:
            print(f'{pilot}:')
            last_end = ProblemData.INITIAL_DATE
            for flight in flights:
                var = flight_pilot_assignment_vars.data[pilot][flight]
                var.flight.start = last_end
                last_end = var.flight.end
                if var.variable.X > 0:
                    print(f'\t{var.flight} - {var.flight.start} - {var.flight.end}')
            print()

        write_solution(flight_pilot_assignment_vars, 'output/solution.xlsx')
        visualize('output/solution.xlsx')
