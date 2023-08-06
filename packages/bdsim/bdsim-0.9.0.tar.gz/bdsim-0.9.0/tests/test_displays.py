#!/usr/bin/env python3

import numpy as np
import math
import copy

import matplotlib.pyplot as plt

from bdsim.blocks.displays import *
from bdsim import BDSim, BDSimState, OptionsBase

import unittest
import numpy.testing as nt


class DisplaysTest(unittest.TestCase):
    
    def test_scope(self):
        
        sim = BDSim(debug='g', animation=True)  # create simulator
        bd = sim.blockdiagram()  # create an empty block diagram
        block = bd.SCOPE(nin=1)
        block.test_inputs = [1]

        state = BDSimState()
        state.options = copy.copy(sim.options)
        state.t = 0
        block.start(state)
        block.step(state)


# ---------------------------------------------------------------------------------------#
if __name__ == '__main__':

    unittest.main()