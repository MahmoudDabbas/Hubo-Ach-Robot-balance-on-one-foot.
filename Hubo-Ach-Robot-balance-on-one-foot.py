import hubo_ach as ha
import ach
import sys
import time
import math
from time import sleep
from ctypes import *
from time import gmtime, strftime

PI = 3.141529
# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
s.flush()
r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

print 'hello'

b=0.18 #define the angle of body tiltig to shift the center of mass.
a=0.01*b #some step
c = 0
while a<=b:
	ref.ref[ha.LEB] = 0
	ref.ref[ha.LSR] = .3 #left arm swing
	ref.ref[ha.RSR] = -.55 #right arm swing
	ref.ref[ha.LAR] = -a
	ref.ref[ha.RAR] = -a
	ref.ref[ha.LHR] = 1.2*a
	ref.ref[ha.RHR] = a
	ref.ref[ha.RHP] = 0
	ref.ref[ha.LHP] = 0
	ref.ref[ha.RKN] = 0
	ref.ref[ha.LKN] = 0
	ref.ref[ha.LAP] = -0
	ref.ref[ha.RAP] = -0
	ref.ref[ha.RSP] = 0 
	ref.ref[ha.LSP] = 0
	time.sleep(0.2)
	a=a+0.02*b
	r.put(ref)
time.sleep(2)

b=PI/3
a=0.01*b
c = 0
while a<=b: # for movemnet smoothing.
	ref.ref[ha.LHP] = -1*a 
	ref.ref[ha.LKN] = 2*a 
	ref.ref[ha.LAP] = -1*a 
	x=time.time()
	r.put(ref)
	print "%.20f" % time.time()
	print c
	c=c+1
	a=a+0.01*b
	time.sleep(.02)

time.sleep(2)

for x in range (1,5):
	b=PI/5
	a=0.01*b
	c = 0
	while a<=b:
		ref.ref[ha.RSP] = 0
		ref.ref[ha.LSP] = 0 
		ref.ref[ha.RHP] = -1*a 
		ref.ref[ha.RKN] = 2*a 
		ref.ref[ha.RAP] = -1*a 
		x=time.time()
		r.put(ref)
		print "%.20f" % time.time()
		print c
		c=c+1
		a=a+0.01*b
		time.sleep(.02)
	time.sleep(0.2)
	while a>=0:
		ref.ref[ha.RSP] = 0
		ref.ref[ha.LSP] = 0 
		ref.ref[ha.RHP] = -1*a 
		ref.ref[ha.RKN] = 2*a 
		ref.ref[ha.RAP] = -1*a 
		x=time.time()
		r.put(ref)
		print "%.20f" % time.time()
		print c
		c=c-1
		a=a-0.01*b
		time.sleep(.02)
	time.sleep(0.2)


ref.ref[ha.LAR] = 0
ref.ref[ha.RAR] = 0
ref.ref[ha.LHR] = 0
ref.ref[ha.RHR] = 0
ref.ref[ha.LAR] = 0
ref.ref[ha.RAR] = 0
ref.ref[ha.RHP] = 0
ref.ref[ha.LHP] = 0
ref.ref[ha.RKN] = 0
ref.ref[ha.LKN] = 0
ref.ref[ha.LAP] = 0 
ref.ref[ha.RAP] = 0 
ref.ref[ha.RSP] = 0 
ref.ref[ha.LSP] = 0 
r.put(ref)

# Close the connection to the channels

r.close()
s.close()

