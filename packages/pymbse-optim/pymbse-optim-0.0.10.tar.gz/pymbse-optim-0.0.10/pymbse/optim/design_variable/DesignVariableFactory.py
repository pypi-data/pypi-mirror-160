from typing import List

import pandas as pd

from pymbse.optim.design_variable.DesignVariable import DesignVariable
from pymbse.optim.design_variable.GeneticDesignVariable import GeneticDesignVariable
from pymbse.commons import json_file


def init_design_variables_with_csv(csv_path: str) -> List[GeneticDesignVariable]:
    """

    :param csv_path:
    :return:
    """
    # todo: add description of columns in the dataframe
    design_variables_df = pd.read_csv(csv_path)
    return init_design_variables_with_df(design_variables_df)


def init_design_variables_with_json(json_path: str) -> list:
    design_variables = json_file.read(json_path)
    return [initialize_design_variable(design_variable) for design_variable in design_variables]


def init_design_variables_with_df(design_variables_df: pd.DataFrame) -> list:
    return [initialize_design_variable(row) for (_, row) in design_variables_df.iterrows()]


def initialize_design_variable(row):
    if 'bits' in row:
        return GeneticDesignVariable(**row)
    else:
        return DesignVariable(**row)
