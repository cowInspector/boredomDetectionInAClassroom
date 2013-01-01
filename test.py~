import pylab
import random
import time

'''
def main():
    pylab.ion()       # Turn on interactive mode.
    pylab.hold(False) # Clear the plot before adding new data.
    x = range(10)
    print x
    y = random.sample(xrange(100), 10)
    pylab.plot(x, y)
    """
    for i in range(10):
        y = random.sample(xrange(100), 10)
        print y
        pylab.plot(x, y)
        time.sleep(1)
    """
    pylab.show()
    
    
if __name__ == '__main__':
    main()
'''

import matplotlib.pyplot as plt
import numpy as np
import time
'''
x = np.linspace(0, 6*np.pi, 100)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()
'''
    
    
    
    
    
    
    
    
    
    

width = 50
x = range(width)
y = random.sample(range(100), width)
plt.ion()

#x = []
#y = []

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y)
line2, = ax.plot(x, y)

a = []
b = []

MyMax = 0
MyMin = 1000000

for i in range(200):
  time.sleep(0.1)
  #y = random.sample(range(100), 10)
  a.append(i*i)
  b.append(i*i*random.random())
  
  if(len(a) < width):
    ax.set_xbound(lower=0, upper=width)
    ax.set_ybound(lower=0, upper=max(a))
    line1.set_xdata(range(len(a)))
    line1.set_ydata(a)
  else:
    ax.set_xbound(lower=len(a) - width, upper=len(a))
    ax.set_ybound(lower=0, upper=max(a[-width:]))
    line1.set_xdata(range(len(a) - width, len(a)))
    line1.set_ydata(a[-width:])
    
  '''
  if(len(b) < width):
    line2.set_xdata(range(len(b)))
    line2.set_ydata(b)
  else:
    line2.set_xdata(len(b) - range(width), len(b))
    line2.set_ydata(b[-width:])
  '''
  
  fig.canvas.draw()





















"""
#from scipy import *
import matplotlib
matplotlib.use('TkAgg')	  #Try this to work best in linux. Or qt4agg, or gtkagg
import pylab
import numpy

'''
x = linspace(0,1,200)       #Defines array of x values from 0 to 1

f = 2
ion()              #Turns interactive mode on.
ans=''
while ans != 'q':
    y = sin(2*pi*f*x)
    plot(x,y,'o-')
    draw()         #Need this to work on linux?

    ans=raw_input('f = '+repr(f)+'. Enter new f, or q: ')
    if ans != 'q':
        f = float(ans)
        clf()       #Clears the figure
ioff()

print 'Remember to close figure window.'
show()
'''

pylab.ion()
x = numpy.array([])
y = numpy.array([])
z = numpy.array([])

for i in range(10):
  pylab.clf()
  Tx = list(x)
  Tx.append(i)
  x = numpy.array(Tx)
  print x
  
  Ty = list(y)
  Ty.append(50 + 100*random.random())
  y = numpy.array(Ty)
  print y
  
  Tz = list(z)
  Tz.append(50 + 100*random.random())
  z = numpy.array(Tz)
  print z
  
  pylab.plot(x, y)
  pylab.plot(x, z)
  time.sleep(0.1)
  pylab.draw()
  
raw_input("")
pylab.ioff()
pylab.show()
"""