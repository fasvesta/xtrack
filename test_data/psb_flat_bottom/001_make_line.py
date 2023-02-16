import numpy as np
from cpymad.madx import Madx
import xtrack as xt
import xpart as xp
import json
import xobjects as xo
import xfields as xf

####################
# Choose a context #
####################

context = xo.ContextCpu()
#context = xo.ContextCupy()
#context = xo.ContextPyopencl('0.0')

mad = Madx()
mad.call('psb_thin_flat_bottom.seq')
mad.use('psb')

line= xt.Line.from_madx_sequence(mad.sequence['psb'],install_apertures=True)
line.particle_ref=xp.Particles(mass0=xp.PROTON_MASS_EV,
                               gamma0=mad.sequence.psb.beam.gamma)

with open('line_and_particle.json', 'w') as fid:
    json.dump(line.to_dict(), fid, cls=xo.JEncoder)

