import time
import numpy as np

from cpymad.madx import Madx

import xtrack as xt
import xpart as xp
import xobjects as xo

# Import a thick sequence
mad = Madx()
mad.call('../../test_data/clic_dr/sequence.madx')
mad.use('ring')

# Makethin
mad.input(f'''
select, flag=MAKETHIN, SLICE=4, thick=false;
select, flag=MAKETHIN, pattern=wig, slice=1;
MAKETHIN, SEQUENCE=ring, MAKEDIPEDGE=true;
use, sequence=RING;
''')
mad.use('ring')

# Build xtrack line
print('Build xtrack line...')
line = xt.Line.from_madx_sequence(mad.sequence['RING'])
line.particle_ref = xp.Particles(
        mass0=xp.ELECTRON_MASS_EV,
        q0=-1,
        gamma0=mad.sequence.ring.beam.gamma)

# Build tracker
print('Build tracker ...')
tracker = xt.Tracker(line=line)

tracker.configure_radiation(mode='quantum')

particles = xp.build_particles(tracker=tracker, x=[0,0,0,0])

tracker.track(particles, num_turns=10)