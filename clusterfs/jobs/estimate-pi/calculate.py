from mpi4py import MPI
from math   import pi as PI
from numpy  import array
from time import process_time

  
start = process_time()


def comp_pi(n, myrank=0, nprocs=1):
    h = 1.0 / n
    s = 0.0
    for i in range(myrank + 1, n + 1, nprocs):
        x = h * (i - 0.5)
        s += 4.0 / (1.0 + x**2)
    return s * h

def prn_pi(pi, PI):
    #message = "pi is approximately %.16f, error is %.16f"
    #print  (message % (pi, abs(pi - PI)))
    print ("pi estimate: %.16f" % (pi))
    print ("error: %.16f" % (abs(pi - PI)))

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

n    = array(0, dtype=int)
pi   = array(0, dtype=float)
mypi = array(0, dtype=float)

if myrank == 0:
    _n = 30000000 # Enter the number of intervals
    n.fill(_n)
comm.Bcast([n, MPI.INT], root=0)
_mypi = comp_pi(n, myrank, nprocs)
mypi.fill(_mypi)
comm.Reduce([mypi, MPI.DOUBLE], [pi, MPI.DOUBLE],
            op=MPI.SUM, root=0)
if myrank == 0:
    prn_pi(pi, PI)
    print('process time (sec):', process_time()-start)
    print('nprocs:', nprocs)
    print('main node:', MPI.Get_processor_name())

