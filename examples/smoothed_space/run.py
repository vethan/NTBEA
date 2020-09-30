import logging
import numpy as np

from ntbea import SearchSpace, Evaluator, NTupleLandscape, NTupleEvolutionaryAlgorithm
from ntbea.common import DefaultMutator


class GaussianSpace(SearchSpace):

    def __init__(self, dims):
        super().__init__("Goldstein Search Space", dims*2)

        mu, sig = self._generate_gaussians_population((0, 0), (1, 1), (0.05, 0.05), (0.1, 0.1), 10)

        self._search_space np.stack(self._mus, self,_sigs)

    def get_value_at(self, idx):
        assert len(idx) == 2
        assert idx[0] < self._ndims
        assert idx[1] < self._m

        return self._search_space[idx]

    def get_random_point(self):
        return np.random.choice(np.arange(1, self._m + 1), size=(self._ndims))

    def get_valid_values_in_dim(self, dim):
        return self._search_space[:, dim]

    def get_size(self):
        return self._m ** self._ndims

    def _generate_gaussians_population(self, min_mu, max_mu, min_sig, max_sig, steps):
        mu = np.linspace(min_mu, max_mu, steps)
        sig = np.linspace(min_sig, max_sig, steps)
        return mu, sig

class GoldsteinEvaluator(Evaluator):

    def __init__(self):
        super().__init__()

    def evaluate(self, x):
        x1 = x[0] * 4.0 - 2.0
        x2 = x[1] * 4.0 - 2.0
        return np.maximum(0, ((400.0 - (1.0 + (x1 + x2 + 1) ** 2 * (
                19.0 - 14 * x1 + 3 * x1 ** 2 - 14 * x2 + 6 * x1 * x2 + 3 * x2 ** 2)) *
                               (30.0 + (2 * x1 - 3 * x2) ** 2 * (
                                       18.0 - 32 * x1 + 12 * x1 ** 2 + 48 * x2 - 36 * x1 * x2 + 27 * x2 ** 2))) / 500.0))