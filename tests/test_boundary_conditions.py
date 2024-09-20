# tests/test_boundary_conditions.py

import unittest
from ..src.models import Node, OpenChannel, PressurizedPipe
from ..src.boundary_conditions import apply_boundary_conditions
from ..src.numerics import free_surface_width

class TestBoundaryConditions(unittest.TestCase):
    def test_inflow_boundary(self):
        node = Node(id=0, flow=OpenChannel(Q=0.0, A=0.0, h=0.0, theta=0.05, S0=0.001, K=50.0, b=2.0), boundary_condition='Inflow', inflow=10.0)
        system = {'0': node}
        apply_boundary_conditions(system)
        self.assertEqual(system['0'].flow.Q, 10.0)
        self.assertEqual(system['0'].flow.h, 10.0 / 2.0)
    
    def test_outflow_boundary(self):
        node = Node(id=1, flow=OpenChannel(Q=0.0, A=0.0, h=0.0, theta=0.05, S0=0.001, K=50.0, b=2.0), boundary_condition='Outflow', outflow=5.0)
        system = {'1': node}
        apply_boundary_conditions(system)
        self.assertEqual(system['1'].flow.Q, 5.0)
        self.assertEqual(system['1'].flow.h, 5.0 / 2.0)
    
    def test_no_boundary_condition(self):
        node = Node(id=2, flow=OpenChannel(Q=10.0, A=2.0, h=5.0, theta=0.05, S0=0.001, K=50.0, b=2.0))
        system = {'2': node}
        apply_boundary_conditions(system)
        self.assertEqual(system['2'].flow.Q, 10.0)  # Should remain unchanged
        self.assertEqual(system['2'].flow.h, 5.0 / 2.0)

if __name__ == '__main__':
    unittest.main()
