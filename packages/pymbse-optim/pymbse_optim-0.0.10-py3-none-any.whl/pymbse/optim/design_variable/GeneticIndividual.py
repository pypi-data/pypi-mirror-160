import hashlib
import json
from copy import deepcopy
from typing import List

from pymbse.optim.design_variable.GeneticDesignVariable import GeneticDesignVariable


class GeneticIndividual:
    def __init__(self, design_variables: List[GeneticDesignVariable]):
        self.design_variables = deepcopy(design_variables)
        self.score = None
        self.fom = {}

    def generate_random_genes(self) -> None:
        for dv in self.design_variables:
            dv.generate_random_gene()

    def is_fom_correct(self):
        return self.fom and all([value is not None for value in self.fom.values()])

    def assemble_chromosome(self) -> List[int]:
        chromosome = []
        for gen_dv in self.design_variables:
            chromosome.extend(gen_dv.gene)

        return chromosome

    def sequence_chromosome(self, chromosome: List[int]) -> None:
        index_start = 0
        for gen_dv in self.design_variables:
            index_end = index_start + gen_dv.bits
            gen_dv.gene = chromosome[index_start: index_end]
            index_start = index_end

    def __str__(self):
        if self.score is None:
            return f"Individual, score: NaN, chromosome: {self.assemble_chromosome()}"
        else:
            return f"Individual, score: {self.score:.2f}, chromosome: {self.assemble_chromosome()}"

    def dict(self):
        return {"genetic_design_variables": [gen_dv.__dict__ for gen_dv in self.design_variables]}

    def __hash__(self):
        return hashlib.md5(json.dumps(self.dict(), sort_keys=True).encode('utf-8')).hexdigest()

    def get_design_variables(self):
        output_design_variables = []
        for design_variable in self.design_variables:
            output_design_variables.append(dict(xl=design_variable.xl,
                                                xu=design_variable.xu,
                                                value=design_variable.value,
                                                variable=design_variable.variable,
                                                variable_type=design_variable.variable_type))

        return output_design_variables

