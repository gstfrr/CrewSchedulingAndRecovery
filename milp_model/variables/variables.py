# -*- coding: utf-8 -*-
"""variables File

This file is used to define the Variable classes to be used in the model. We have the main Abstract class Variable, then
we define the others.The usage of a class for each variable is to make the code more readable and easy to understand,
and it also provides direct access to the variable indexes, to be used later with the dictionaries.
"""

from abc import ABC, abstractmethod
from gurobipy import Model, GRB
from ProblemData import ProblemData


class Variable(ABC):
    """Main abstract class for the variables."""

    def __init__(self, objective=0):
        self.variable = None
        self.objective = objective

    @abstractmethod
    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        pass

    @property
    def name(self):
        """ """
        return self.__repr__()


class StartTimeVar(Variable):
    """ """

    def __init__(self, model, pilot, flight, objective=0):
        super().__init__(objective=objective)
        self.pilot = pilot
        self.flight = flight
        self.duration = self.flight.duration

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.CONTINUOUS, obj=self.objective)

    def __repr__(self):
        return f'StartTimeVar{self.pilot}_{self.flight}'


class PrecedenceVar(Variable):

    def __init__(self, model, pilot, flight1, flight2, objective=0):
        super().__init__(objective=objective)
        self.pilot = pilot
        self.flight1 = flight1
        self.flight2 = flight2

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, ub=1.0)

    def __repr__(self):
        return f'PrecedenceVar_({self.pilot})_({self.flight1})_({self.flight2})'


class FlightPilotAssignmentVar(Variable):
    """ """

    def __init__(self, model, pilot, flight, objective=0):
        super().__init__(objective=objective)
        self.pilot = pilot
        self.flight = flight

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self):
        return f'FlightPilotAssignment_{self.pilot}_{self.flight}'


class PilotPairingAssignmentVar(Variable):
    """ """

    def __init__(self, model, pilot, pairing, objective):
        super().__init__(objective=objective)
        self.pilot = pilot
        self.pairing = pairing

        self.variable = self._add_variable(model=model)

    def _add_variable(self, model: Model):
        """This is the function that will invoke the Gurobi function to add the variable to the model.

        :param model: Model: Gurobi model.

        """
        return model.addVar(name=self.name, vtype=GRB.BINARY, obj=self.objective)

    def __repr__(self):
        return f'PilotPairingAssignment_{self.pilot}_{self.pairing}'
