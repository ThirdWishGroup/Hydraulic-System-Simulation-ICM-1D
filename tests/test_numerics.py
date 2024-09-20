# tests/test_numerics.py

import unittest
from src.numerics import continuity_equation, momentum_equation, preissmann_scheme, free_surface_width, apply_preissmann_slot
from src.models import OpenChannel, PressurizedPipe

class TestNumerics(unittest.TestCase):
    def test_continuity_equation(self):
        # Example where residual should be zero
        residual = continuity_equation(A_current=2.1, A_previous=2.0, Q_current=10.1, Q_previous=10.0, delta_t=1.0, delta_x=1.0)
        self.assertAlmostEqual(residual, 0.0, places=5)
    
    def test_momentum_equation(self):
        # Example where residual should be zero
        residual = momentum_equation(Q_current=10.1, Q_previous=10.0, A_current=2.1, A_previous=2.0,
                                     h_current=5.05, h_previous=5.0, theta=0.1, S0=0.05, K=100.0,
                                     delta_t=1.0, delta_x=1.0)
        # Depending on exact computations, adjust the expected residual
        self.assertAlmostEqual(residual, 0.0, places=2)  # Adjust places based on expected precision
    
    def test_preissmann_scheme(self):
        result = preissmann_scheme(theta=0.5, f_current=10.0, f_next=12.0)
        expected = (0.5 / 2) * 12.0 + ((1 - 0.5) / 2) * (10.0 + 10.0)  # = 3 + 5 = 8
        self.assertAlmostEqual(result, 8.0, places=5)
    
    def test_free_surface_width(self):
        B = free_surface_width(Af=4.5, Cp=150.0)
        expected = (9.81 * 4.5) / (150.0 ** 2)
        self.assertAlmostEqual(B, expected, places=5)
    
    def test_cfl_condition(self):
        from src.numerics import apply_cfl_condition
        self.assertTrue(apply_cfl_condition(theta=0.5, delta_t=1.0, delta_x=2.0))
        self.assertFalse(apply_cfl_condition(theta=1.0, delta_t=2.0, delta_x=1.0))

if __name__ == '__main__':
    unittest.main()
