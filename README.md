# CrewSchedulingAndRecovery

## How is this solver implemented?

1. The program uses an Excel sheet as input
2. The ProblemData class processes the input and creates some lists with entities:
    1. `flights` - list of Flight objects
    2. `crews` - list of Pilot objects
    3. `pairings` - list of pairings generated from the flights. Check pairing_generator.py for more details.
    4. The ProblemData class also sets some parameters like costs and others.
3. The problem data is sent to the optimization process in the form of a dictionary.
4. The optimization process is done as usual:
    1. model creation,
    2. variables,
    3. constraints,
    4. optimization,
    5. process solution.