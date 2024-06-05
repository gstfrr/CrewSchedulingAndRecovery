import os
from timeit import default_timer as timer

from ProblemData import ProblemData
from milp_model.milp_model import get_optimization

if not os.path.exists('output/'):
    os.mkdir('output/')


def main():
    """ """
    file_path = 'instances/instance1.xlsx'
    # input_data = read_excel(file_path)
    input_data = ''
    problem_data = ProblemData.basic_process(input_data)

    start = timer()

    get_optimization(problem_data)

    end = timer()
    print(f'\tOptimization time: {end - start} seconds')


if __name__ == '__main__':
    main()
