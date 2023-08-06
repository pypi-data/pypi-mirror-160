import unittest

import sympy as sp
from sympy.matrices import eye
from tensors.indexed import IndexObject, Manifold, NotContainedSymbolException
from tensors.indexed import Tensor, ChristoffelSymbol


class IndexedTest(unittest.TestCase):

    def test_display(self):
        # Act
        x, y = sp.symbols("x, y")
        vector = IndexObject(r"\phi", (x, y), {(x, x): 1, (y, y): 2})

        actual = vector.display()
        expected = r"$$\phi_x{}_x = 1 \\ \phi_y{}_y = 2$$"
        # Assert
        self.assertEqual(expected, actual)

    def test_get_item(self):
        # Act
        x, y = sp.symbols("x, y")
        vector = IndexObject(r"\phi", (x, y), {(x, x): 1, (y, y): 2})
        actual = vector[x, x]
        # Assert
        self.assertEqual(1, actual)

    def test_display_three(self):
        # Arrange
        x, y, z = sp.symbols("x, y, z")
        vector = IndexObject(r"\phi", (x, y, z), {(x, x, x): 1, (y, y, y): 2, (y, z, z): 3})

        # Act
        actual = vector.display()
        expected = r"$$\phi_x{}_x{}_x = 1 \\ \phi_y{}_y{}_y = 2 \\ \phi_y{}_z{}_z = 3$$"

        # Assert
        self.assertEqual(actual, expected)

    def test_non_given_coordinate(self):
        # Act
        x, y = sp.symbols("x, y")
        vector = IndexObject(r"\phi", (x, y), {(x, x): 1, (y, y): 2})

        actual = vector[x, y]
        # Assert
        self.assertEqual(0, actual)

    def test_non_contained_coordinate(self):
        # Act
        x, y, z = sp.symbols("x, y,z")
        vector = IndexObject(r"\phi", (x, y), {(x, x): 1, (y, y): 2})
        with self.assertRaises(NotContainedSymbolException):
            vector[x, z]

    def test_non_contained_coordinate_constructor(self):
        # Act
        x, y, z = sp.symbols("x, y,z")
        with self.assertRaises(NotContainedSymbolException):
            vector = IndexObject(r"\phi", (x, y), {(x, z): 1, (y, y): 2})

    def test_display_1up2down(self):
        # Arrange
        x, y, z = sp.symbols("x, y, z")
        vector = IndexObject(r"\phi", (x, y, z), {(x, x, x): 1, (y, y, y): 2, (y, z, z): 3}, index_pos=(1, 0, 0))

        # Act
        actual = vector.display()
        expected = r"$$\phi^x{}_x{}_x = 1 \\ \phi^y{}_y{}_y = 2 \\ \phi^y{}_z{}_z = 3$$"

        # Assert
        self.assertEqual(actual, expected)


class ManifoldTest(unittest.TestCase):

    def test_init(self):
        x, y, z = sp.symbols("x, y, z")
        coords = (x, y, z)
        manifold = Manifold(coords,
                            {(x, x): 1, (y, y): 1, (z, z): 1})

        assert manifold.coords == coords
        assert type(manifold.metric) == Tensor

    def test_convert_sympy_matrix(self):
        # Arrange
        x, y, z = sp.symbols("x, y, z")
        coords = (x, y, z)
        manifold = Manifold(coords,
                            {(x, x): 1, (y, y): 1, (z, z): 1})

        # Act
        actual = manifold.metric_to_matrix()
        expected = eye(3)

        # Assert
        self.assertEqual(actual, expected)

    def test_manifold_from_matrix(self):
        # Arrange
        matrix = eye(3)

        # Act
        x, y, z = sp.symbols("x, y, z")
        coords = (x, y, z)
        actual = Manifold(coords, matrix)
        expected = Manifold(coords,
                            {(x, x): 1, (y, y): 1, (z, z): 1})

        # Assert
        assert actual.metric.display() == expected.metric.display()


class TensorTest(unittest.TestCase):
    def test_init(self):
        x, y, z = sp.symbols("x, y, z")
        coords = (x, y, z)
        manifold = Manifold(coords,
                            {(x, x): 1, (y, y): 1, (z, z): 1})
        tensor = Tensor(r"\phi",
                        manifold,
                        (0, 0),
                        {(x, x): 1, (x, y): 2, (z, z): 3})

        assert tensor.coords == coords
        assert tensor.manifold is not None

        actual = tensor[x, y]
        # Assert
        self.assertEqual(2, actual)


class ChristoffelSymbolTest(unittest.TestCase):
    def test_init(self):
        x, y, z = sp.symbols("x, y, z")
        coords = (x, y, z)

        manifold = Manifold(coords,
                            {(x, x): 1, (y, y): 1, (z, z): 1})
        cs = ChristoffelSymbol(manifold)

        assert cs.values == {}

    def test_polar_coords(self):
        rho, theta = sp.symbols(r"\rho, \theta")
        coords = (rho, theta)

        manifold = Manifold(coords,
                            {(rho, rho): 1, (theta, theta): rho ** 2})
        cs = ChristoffelSymbol(manifold)
        print(cs.values)
        true_values={(rho, theta, theta): -1.0*rho, (theta, rho, theta): 1.0/rho, (theta, theta, rho): 1.0 / rho}
        print(true_values)
        assert cs.values == true_values


if __name__ == '__main__':
    unittest.main()
