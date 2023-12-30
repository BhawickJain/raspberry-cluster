# Next Steps

I want to make the most out learning about parallelism and algorithms that need
parallelism. However I want to minimise technical overhead as specific
build/implementations have plenty of gotcha's. My setup details the shortest
path to creating a test bench for what is a fairly tricky, yet exciting topic.

The ultimate aim is to develop and understand examples, and perhaps write
something myself, that are a wee bit above trivial:
 - parallelism in algorithms and different kinds of parallelism
 - concurrency if or when it makes sense
 - parallelism without SLURM/MPI with plain-old `process` spawning, and
   multi-threading for concurrent problems.
 - coordination of process on the same node and across nodes


## Resources

The following is a collection of nice resource I came across whilst building
the cluster. I have a mental note on what each holds so I don't want to be
searching for them again:

Familiarising with MPI and dealing with the consequences of parallelism:
 - [MPI exercises with solutions by Rold Rabensifner](https://www.hlrs.de/training/par-prog-ws/MPI-course-material)
 - [Parallel Programming for Science and Engineering by Victor Eijkhout](https://tinyurl.com/vle335course) [[HTML Format]](https://tacc.utexas.edu/~eijkhout/pcse/html/index.html)
 - [mpi4py get started tutorial](https://mpi4py.readthedocs.io/en/stable/tutorial.html)
 - [mpi4py's overview on how python objects are passed between processes](https://mpi4py.readthedocs.io/en/stable/overview.html#communicating-python-objects-and-array-data)
 - [A comprehensive MPI tutorial resource by Wes Kendall (unmaintained)](https://mpitutorial.com/) [[github]](https://github.com/mpitutorial/mpitutorial)

Using [Dask](https://docs.dask.org/en/stable/deploying-hpc.html) to quickly
take adantage of parallelism across nodes with a 'drop-in' replacement api
for libraries like `numpy`.

Better understanding SLURM:
 - [`SBATCH` directive explained by New Mexico State University](https://hpc.nmsu.edu/discovery/slurm/commands/)
 - [Conda virtual environments inside `SBATCH`](https://hpc.nmsu.edu/discovery/software/conda/virtual-env/)
 - [`man sbatch`](https://manpages.ubuntu.com/manpages/trusty/man1/squeue.1.html) has a nice list of `Job State Codes`
 - [SLURM FAQ](https://slurm.schedmd.com/faq.html#user_env)

Understanding SLURM cluster in the context of portals for users / public to see
the progress of a job like the
[`slurm-web`](https://github.com/rackslab/slurm-web) which had been sponsored
by [`EDF`](https://www.edf.fr/en) and [Rackslab](https://github.com/rackslab).
Work like especially comes together with the rest of experience consisting of
web development. The [software architecture of
`slurm-web`](https://rackslab.github.io/slurm-web/architecture.html) is
especially interesting.

