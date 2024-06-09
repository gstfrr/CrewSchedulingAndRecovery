# -*- coding: utf-8 -*-
"""variables File

This file is used to define the Variable classes to be used in the model. We have the main Abstract class Variable, then
we define the others.The usage of a class for each variable is to make the code more readable and easy to understand,
and it also provides direct access to the variable indexes, to be used later with the dictionaries.
"""

from abc import ABC, abstractmethod
from gurobipy import Model, GRB, Var
from Domain import Flight, Pilot, Pairing


class Variable(ABC):
    """Main abstract class for the variables."""

    def __init__(self, objective: float = 0.0) -> None:
        self.variable = None
        self.objective = objective

    @abstractmethod
    def _add_variable(self, model: Model) -> Var:
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        pass

    @property
    def name(self) -> str:
        """ """
        return self.__repr__()


class FlightPilotAssignmentVar(Variable):
    """ """

    def __init__(self, model: Model, pilot: Pilot, flight: Flight, objective=0) -> None:
        super().__init__(objective=objective)
        self.pilot = pilot
        self.flight = flight

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model) -> Var:
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self) -> str:
        return f'FlightPilotAssignment_{self.flight}_{self.pilot}'


class PairingPilotAssignmentVar(Variable):
    """ """

    def __init__(self, model: Model, pilot: Pilot, pairing: Pairing, objective: float) -> None:
        super().__init__(objective=objective)
        self.pilot = pilot
        self.pairing = pairing

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model) -> Var:
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """

        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self) -> str:
        return f'PairingPilotAssignment_{self.pairing.name}_{self.pilot}'


class PairingFlightAssignmentVar(Variable):
    """ """

    def __init__(self, model: Model, flight: Pilot, pairing: Pairing, objective: float) -> None:
        super().__init__(objective=objective)
        self.pairing = pairing
        self.flight = flight

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model) -> Var:
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self) -> str:
        return f'PairingFlightAssignment_{self.pairing.name}_{self.flight}'


class PairingFlightPilotAssignmentVar(Variable):
    """ """

    def __init__(self, model, flight: Flight, pairing: Pairing, pilot: Pilot, objective: float) -> None:
        super().__init__(objective=objective)
        self.pairing = pairing
        self.flight = flight
        self.pilot = pilot

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model) -> Var:
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self) -> str:
        return f'PairingFlightPilotAssignment_{self.pairing.name}_{self.flight}_{self.pilot}'
