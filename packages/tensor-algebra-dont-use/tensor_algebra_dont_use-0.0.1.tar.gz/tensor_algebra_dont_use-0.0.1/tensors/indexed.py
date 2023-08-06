import numpy as np
import sympy as sp
from sympy.matrices import Matrix

class NotContainedSymbolException(Exception):
    ...


class IndexObject:

    def __init__(self, head, coords, values, index_pos=None):
        self.head = head
        self.coords = coords
        self.values = values
        if index_pos is None:
            index_pos = len(list(values.keys())[0]) * [0]
        self.index_pos = index_pos

        for key in values:
            self.check_valid_index(key)

    def display(self):
        display_parts = []
        for k, v in self.values.items():
            index_strings = []
            for index_pos, k_i in zip(self.index_pos, k):
                index_location = "_" if index_pos == 0 else "^"
                index_strings.append(index_location + sp.latex(k_i))
            display_parts.append(self.head + "{}".join(index_strings) + " = " + str(v))
        dollar = "$$"
        return dollar + r" \\ ".join(display_parts) + dollar

    def __getitem__(self, item):
        self.check_valid_index(item)
        return self.values.get(item, 0)

    def __setitem__(self, item, value):
        self.check_valid_index(item)
        if value != 0:
            self.values[item] = value
        else:
            if item in self.values:
                del self.values[item]

    def check_valid_index(self, index_list):
        assert len(index_list) == len(self.index_pos), "Values for all indices should be specified."
        for symbol in index_list:
            if symbol not in self.coords:
                raise NotContainedSymbolException


class Manifold:

    def __init__(self, coords, metric_values):
        self.coords = coords
        if type(metric_values) == dict:
            values = metric_values

        elif type(metric_values) == Matrix:
            values = self.matrix_to_dict(metric_values)
        else:
            raise TypeError()

        self.metric = Tensor(
            head="g",
            manifold=self,
            index_pos=(0, 0),
            values=values)

        self.metric_inv = Tensor(self.metric.head,
                                 self, (1, 1),
                                 self.matrix_to_dict(self.metric_to_matrix().inv()))

    def matrix_to_dict(self, metric_values):
        values = {}
        size = sp.shape(metric_values)[0]
        for i in range(size):
            for j in range(size):
                if metric_values[i, j] != 0:
                    values[self.coords[i], self.coords[j]] = metric_values[i, j]
        return values

    def metric_to_matrix(self):
        size = len(self.coords)
        mat = Matrix(np.zeros([size, size]))

        for i in range(size):
            for j in range(size):
                mat[i, j] = self.metric[self.coords[i], self.coords[j]]

        return mat


class Tensor(IndexObject):

    def __init__(self, head, manifold, index_pos, values):
        self.manifold = manifold
        super(Tensor, self).__init__(
            head,
            manifold.coords,
            values,
            index_pos=index_pos)


class ChristoffelSymbol(IndexObject):
    def __init__(self, manifold):
        self.manifold = manifold
        g = self.manifold.metric
        coords = self.manifold.coords
        g_inv = self.manifold.metric_inv

        super(ChristoffelSymbol, self).__init__(r"\Gamma", manifold.coords, {}, index_pos=(1, 0, 0))
        for i_mu in coords:
            for i_alpha in coords:
                for i_beta in coords:
                    for i_sigma in coords:
                        self[(i_mu, i_alpha, i_beta)] = self[(i_mu, i_alpha, i_beta)] + 0.5 * g_inv[
                            i_mu, i_sigma] * (sp.diff(g[i_alpha, i_sigma], i_beta)
                                              + sp.diff(g[i_sigma, i_beta], i_alpha)
                                              - sp.diff(g[i_alpha, i_beta], i_sigma))
