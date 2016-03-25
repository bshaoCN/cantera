"""
A burner-stabilized lean premixed hydrogen-oxygen flame at low pressure.
"""

import cantera as ct
import numpy as np

p = 0.05 * ct.one_atm
tburner = 373.0
mdot = 0.06
reactants = 'H2:1.5, O2:1, AR:7'  # premixed gas composition

width = 0.5 # m
loglevel = 1  # amount of diagnostic output (0 to 5)
refine_grid = 1  # 1 to enable refinement, 0 to disable

gas = ct.Solution('h2o2.xml')
gas.TPX = tburner, p, reactants

f = ct.BurnerFlame(gas, width=width)
f.burner.mdot = mdot

f.set_initial_guess()
f.show_solution()

f.energy_enabled = False
f.transport_model = 'Mix'
f.solve(loglevel, refine_grid=False)
f.save('h2_burner_flame.xml', 'no_energy',
       'solution with the energy equation disabled')

f.set_refine_criteria(ratio=3.0, slope=0.05, curve=0.1)
f.energy_enabled = True
f.solve(loglevel, refine_grid)
f.save('h2_burner_flame.xml', 'energy',
       'solution with the energy equation enabled')

#print('mixture-averaged flamespeed = ', f.u[0])

f.transport_model = 'Multi'
f.solve(loglevel, refine_grid)
f.show_solution()
print('multicomponent flamespeed = ', f.u[0])
f.save('h2_burner_flame.xml','energy_multi',
       'solution with the energy equation enabled and multicomponent transport')

f.write_csv('h2_burner_flame.csv', quiet=False)
