# -*- coding: utf-8 -*-
"""variables File

This file is used to define and implement the variables used in the optimization.
"""
import itertools
from gurobipy import Model

from ProblemData import ProblemData, DataDictionary
from Domain import Flight, Pairing, Pilot
from milp_model.variables.variables import FlightPilotAssignmentVar
from milp_model.variables.variables import PairingPilotAssignmentVar
from milp_model.variables.variables import PairingFlightAssignmentVar
from milp_model.variables.variables import PairingFlightPilotAssignmentVar


def create_flight_pilot_assignment_var(model: Model, pilots: list[Pilot], flights: list[Flight]) -> DataDictionary:
    """This function will create a dictionary that stores the variables for the Flight-Pilot assignment. If the pilot
    was originally assigned to the flight, it will receive the objective function coefficient 1. Otherwise it will be
    assigning a unassigned flight and will receive the cost for that.

    :param model: Model: Gurobi model to store the variables.
    :param pilots: list[Pilot]: list of pilots from the ProblemData.
    :param flights: list[Flight]: list of flights from the ProblemData.

    """
    flight_pilot_assignment_vars = DataDictionary()

    pairs = itertools.product(flights, pilots)

    for flight, pilot in pairs:
        obj = ProblemData.UNASSIGNED_FLIGHT
        if flight.pilot == pilot:
            obj = 1
        var = FlightPilotAssignmentVar(model, pilot=pilot, flight=flight, objective=obj)
        flight_pilot_assignment_vars.data[flight][pilot] = var

    return flight_pilot_assignment_vars


def create_pairing_pilot_var(model: Model, pilots: list[Pilot], pairings: list[Pairing],
                             cic_table: DataDictionary) -> DataDictionary:
    """This function will create a binary variable with 2 indexes: pairing and pilot. If the pilot was originally
    assigned to the pairing, the objective function value will receive 1. If not, it will receive the pilot schedule
    changed cost.

    :param model: Model: Gurobi model to store the variables.
    :param pilots: list[Pilot]: list of pilots from the ProblemData.
    :param pairings: list[Pairing]: list of pairings from the ProblemData.
    :param cic_table: DataDictionary: dictionary with binary values. Cic = 1 if and only if pairing i was on original
    schedule of crew c.

    """
    pairing_pilot_vars = DataDictionary()
    for pairing, pilot in itertools.product(pairings, pilots):
        obj = ProblemData.PILOT_SCHEDULE_CHANGED
        if cic_table.data[pairing][pilot]:
            obj = 1
        var = PairingPilotAssignmentVar(model, pairing=pairing, pilot=pilot, objective=obj)
        pairing_pilot_vars.data[pairing][pilot] = var

    return pairing_pilot_vars


def create_pairing_flight_var(model: Model, flights: list[Flight], pairings: list[Pairing],
                              pif_table: DataDictionary) -> DataDictionary:
    """This function will create a binary variable with 2 indexes: pairing and flight. If the flight was originally
    included to the pairing, the objective function value will receive 1. If not, it will receive the assigning pairing
    cost.

    :param model: Model: Gurobi model to store the variables.
    :param flights: list[Flight]: list of flights from the ProblemData.
    :param pairings: list[Pairing]: list of pairings from the ProblemData.
    :param pif_table: DataDictionary: dictionary with binary values. Pif = 1 if and only if pairing i includes flight f.

    """
    # TODO: check this coefficients.
    pairing_flight_vars = DataDictionary()
    for pairing, flight in itertools.product(pairings, flights):
        obj = ProblemData.ASSIGNING_PAIRING  # Assigning unplanned pairing
        if pif_table.data[pairing][flight]:
            obj = ProblemData.UNASSIGNING_PAIRING  # Unassigning original pairing
        var = PairingFlightAssignmentVar(model, pairing=pairing, flight=flight, objective=obj)
        pairing_flight_vars.data[pairing][flight] = var

    return pairing_flight_vars


def create_pairing_flight_pilot_var(model: Model, pilots: list[Pilot], pairings: list[Pairing]) -> DataDictionary:
    """This function will create a binary variable with 3 indexes: pairing, flight and pilot.

    :param model: Model: Gurobi model to store the variables.
    :param pilots: list[Pilot]: list of pilots from the ProblemData.
    :param pairings: list[Pairing]: list of pairings from the ProblemData.

    """
    pairing_flight_pilot_vars = DataDictionary()
    for pairing, pilot in itertools.product(pairings, pilots):
        obj = 0
        for flight in pairing.flights:
            var = PairingFlightPilotAssignmentVar(model, pairing=pairing, flight=flight, pilot=pilot, objective=obj)
            pairing_flight_pilot_vars.data[pairing][flight][pilot] = var

    return pairing_flight_pilot_vars
