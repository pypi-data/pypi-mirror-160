from typing import Union

from pymbse.optim.design_variable.DesignVariableBase import DesignVariableBase


class DesignVariable(DesignVariableBase):
    """ A DesignVariable class for optimization purposes
    """

    def __init__(self,
                 xl: Union[int, float],
                 xu: Union[int, float],
                 variable: str,
                 variable_type: str,
                 x0=0,
                 value=0) -> None:
        """ A DesignVariable constructor

        :param xl: lower limit of a design variable
        :param xu: upper limit of a design variable
        :param variable: name of a design variable
        :param variable_type: numerical type of a variable: either int or float
        """
        super().__init__(xl=xl, xu=xu, variable=variable, variable_type=variable_type)
        self.x0=x0
        self.value = value
