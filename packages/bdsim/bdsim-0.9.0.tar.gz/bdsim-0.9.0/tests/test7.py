import bdsim

sim = bdsim.BDSim(animation=False)

ss = sim.blockdiagram(name='subsystem1')

f = ss.FUNCTION(lambda x: x)
inp = ss.INPORT(1)
outp = ss.OUTPORT(1)

ss.connect(inp, f)
ss.connect(f, outp)

# create main system
bd = sim.blockdiagram()

const = bd.CONSTANT(1)
scope = bd.SCOPE()

ff = bd.SUBSYSTEM(ss, name='subsys')

bd.connect(const, ff)
bd.connect(ff, scope)

bd.compile(verbose=False)