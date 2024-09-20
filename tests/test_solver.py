# tests/test_solver.py

import unittest
from src.models import OpenChannel, PressurizedPipe, Node
from src.solver import HydraulicSystem, solve_hydraulic_system
from src.utilities import initialize_nodes, add_connection


class TestSolver(unittest.TestCase):
    def setUp(self):
        # Initialize a simple hydraulic system with 3 nodes
        num_nodes = 3
        delta_x = 1.0
        delta_t = 0.5
        theta = 0.5
        C_p = 300.0
        time_steps = 1
        slot_area = 0.01
        
        # Initialize nodes as OpenChannel
        nodes = initialize_nodes(num_nodes, channel_type='OpenChannel')
        
        # Define connections with beta coefficients
        beta = {i: {} for i in range(num_nodes)}
        add_connection(beta, 1, 0, 0.5)
        add_connection(beta, 1, 2, 0.5)
        
        # Create HydraulicSystem instance
        self.system = HydraulicSystem(
            nodes=nodes,
            beta=beta,
            delta_x=delta_x,
            delta_t=delta_t,
            theta=theta,
            C_p=C_p,
            time_steps=time_steps,
            slot_area=slot_area
        )
    
    def test_solver_convergence_open_channel(self):
        # Run the solver
        try:
            solve_hydraulic_system(self.system)
            # Check if internal node has updated values
            internal_node = self.system.nodes[1]
            self.assertNotEqual(internal_node.flow.Q, 10.0)
            self.assertNotEqual(internal_node.flow.A, 2.0)
        except Exception as e:
            self.fail(f"Solver raised an exception: {e}")
    
    def test_solver_convergence_pressurized_pipe(self):
        # Modify system to PressurizedPipe
        for node in self.system.nodes.values():
            if isinstance(node.flow, OpenChannel):
                node.flow = PressurizedPipe(Q=node.flow.Q, A=node.flow.A, h=node.flow.h, Af=4.0, Cp=300.0, B=0.0)
        
        # Run the solver
        try:
            solve_hydraulic_system(self.system)
            # Check if internal node has updated values
            internal_node = self.system.nodes[1]
            self.assertNotEqual(internal_node.flow.Q, 10.0)
            self.assertNotEqual(internal_node.flow.A, 2.0)
            self.assertGreater(internal_node.flow.B, 0.0)
        except Exception as e:
            self.fail(f"Solver raised an exception: {e}")
    
    def test_solver_no_internal_nodes(self):
        # Initialize system with only boundary nodes
        num_nodes = 2
        nodes = initialize_nodes(num_nodes, channel_type='OpenChannel')
        beta = {}
        system = HydraulicSystem(
            nodes=nodes,
            beta=beta,
            delta_x=1.0,
            delta_t=0.5,
            theta=0.5,
            C_p=300.0,
            time_steps=1,
            slot_area=0.01
        )
        
        # Run the solver
        try:
            solve_hydraulic_system(system)
            # Ensure no changes since there are no internal nodes
            self.assertEqual(system.nodes[0].flow.Q, 10.0)
            self.assertEqual(system.nodes[1].flow.Q, 10.0)
        except Exception as e:
            self.fail(f"Solver raised an exception: {e}")



if __name__ == '__main__':
    unittest.main()
