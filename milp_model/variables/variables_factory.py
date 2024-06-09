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
    pairing_flight_vars = DataDictionary()
    for pairing, flight in itertools.product(pairings, flights):
        obj = ProblemData.ASSIGNING_PAIRING  # Assigning unplanned pairing
        if pif_table.data[pairing][flight]:
            obj = ProblemData.UNASSIGNING_PAIRING  # Unassigning original pairing
        var = PairingFlightAssignmentVar(model, pairing=pairing, flight=flight, objective=obj)
        pairing_flight_vars.data[pairing][flight] = var

    return pairing_flight_vars


def create_pairing_flight_pilot_var(model: Model, pilots: list[Pilot], pairings: list[Pairing]) -> DataDictionary:
    pairing_flight_pilot_vars = DataDictionary()
    for pairing, pilot in itertools.product(pairings, pilots):
        obj = 0
        for flight in pairing.flights:
            var = PairingFlightPilotAssignmentVar(model, pairing=pairing, flight=flight, pilot=pilot, objective=obj)
            pairing_flight_pilot_vars.data[pairing][flight][pilot] = var

    return pairing_flight_pilot_vars
