# tests/test_models.py

import unittest
from src.models import Flow, OpenChannel, PressurizedPipe

class TestModels(unittest.TestCase):
    def test_flow_creation(self):
        flow = Flow(Q=10.0, A=2.0, h=5.0)
        self.assertEqual(flow.Q, 10.0)
        self.assertEqual(flow.A, 2.0)
        self.assertEqual(flow.h, 5.0)
    
    def test_open_channel_creation(self):
        open_channel = OpenChannel(Q=15.0, A=3.0, h=6.0, theta=0.1, S0=0.05, K=50.0, b=3.0)
        self.assertEqual(open_channel.theta, 0.1)
        self.assertEqual(open_channel.S0, 0.05)
        self.assertEqual(open_channel.K, 50.0)
        self.assertEqual(open_channel.b, 3.0)
    
    def test_pressurized_pipe_creation(self):
        pressurized_pipe = PressurizedPipe(Q=20.0, A=4.0, h=7.0, Af=4.5, Cp=150.0, slot_area=0.02)
        self.assertEqual(pressurized_pipe.Af, 4.5)
        self.assertEqual(pressurized_pipe.Cp, 150.0)
        self.assertEqual(pressurized_pipe.slot_area, 0.02)

if __name__ == '__main__':
    unittest.main()
