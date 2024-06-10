# -*- coding: utf-8 -*-
"""Main File"""
import os
from timeit import default_timer as timer
import pandas as pd

from ProblemData import ProblemData
from milp_model.milp_model import get_optimization

if not os.path.exists('output/'):
    os.mkdir('output/')


def read_excel(file_path: str) -> dict:
    """

    :param file_path: str: excel file with thee input data. The input date are the pilots names,
    a list of flights and a set of parameters and values.

    """
    excel_data = pd.ExcelFile(file_path)
    data_dict = {}

    # Iterate through each sheet and convert rows to dictionary objects
    for sheet in excel_data.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        data_dict[sheet] = df.to_dict(orient='records')

    return data_dict


def main() -> None:
    """The program starts here. It reads the input data from an excel file and processes it."""
    file_path = 'instances/instance1.xlsx'
    input_data = read_excel(file_path)
    problem_data = ProblemData.basic_process(input_data)

    start = timer()
    get_optimization(problem_data)
    end = timer()
    print(f'\tOptimization time: {end - start} seconds')


if __name__ == '__main__':
    main()
