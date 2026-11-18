import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))
from ode_methods import solve

class MethodTests(unittest.TestCase):
    def test_decay_amplification(self):
        for method in ('euler', 'rk4'):
            t, y = solve(lambda t, y: -y, 1, 0, 2, 20, method)
            z = -0.1
            factor = 1+z if method == 'euler' else 1+z+z*z/2+z**3/6+z**4/24
            np.testing.assert_allclose(y, factor**np.arange(21), atol=1e-14)

    def test_nonautonomous_problem(self):
        t, y = solve(lambda t, y: 2*t, 0, 0, 2, 20, 'rk4')
        np.testing.assert_allclose(y, t*t, atol=1e-13)

    def test_orders(self):
        for method, expected in [('euler',1), ('rk4',4)]:
            errors = []
            for n in (80, 160):
                t,y = solve(lambda t,y: -y,1,0,2,n,method)
                errors.append(max(abs(y-np.exp(-t))))
            self.assertAlmostEqual(np.log2(errors[0]/errors[1]), expected, delta=0.1)

    def test_invalid_inputs(self):
        for n in (0, -1, 2.5, True):
            with self.assertRaises(ValueError):
                solve(lambda t,y: -y,1,0,2,n)
        with self.assertRaises(ValueError):
            solve(lambda t,y: -y,1,0,2,20,'unknown')

if __name__ == '__main__':
    unittest.main()
