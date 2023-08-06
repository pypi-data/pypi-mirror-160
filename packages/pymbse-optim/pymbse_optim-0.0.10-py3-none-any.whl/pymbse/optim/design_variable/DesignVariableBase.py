from typing import Union


class DesignVariableBase:
    """ A DesignVariable class for optimization purposes
    """

    def __init__(self,
                 xl: Union[int, float],
                 xu: Union[int, float],
                 variable: str,
                 variable_type: str) -> None:
        """ A DesignVariable constructor

        :param xl: lower limit of a design variable
        :param xu: upper limit of a design variable
        :param variable: name of a design variable
        :param variable_type: numerical type of a variable: either int or float
        """
        self.variable_type = variable_type
        conversion_method = int if variable_type == 'int' else float
        self.xl = conversion_method(xl)
        self.xu = conversion_method(xu)
        self.variable = variable

    def get_compact_variable_name(self) -> str:
        return self.variable

    def get_hover_text(self, value) -> str:
        if self.variable_type == 'float':
            return 'value: %.3f, range: [%.3f, %.3f]' % (value, self.xl, self.xu)
        else:
            return 'value: %d, range: [%d, %d]' % (value, self.xl, self.xu)

    def get_fraction(self, value) -> float:
        if self.xu == self.xl:
            return 1
        else:
            return (value - self.xl) / (self.xu - self.xl)
