I have relied on a number of resources, below is a list I have found helpful.
It is fairly unstructured at the moment.

### References
- Gareth Mills articles: 
  - [Part I](https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd)
  - [Part II](https://glmdev.medium.com/building-a-raspberry-pi-cluster-aaa8d1f3d2ca)
  - [Part III](https://glmdev.medium.com/building-a-raspberry-pi-cluster-f5f2446702e8)
- [Benchmarking a Turing Pi Cluster by Jeff Geerling](https://www.youtube.com/watch?v=IoMxpndlDWI)
- [Raspberry Pi Cluster Ep 1 - Introduction to Clustering](https://www.youtube.com/watch?v=kgVz4-SEhbE)
- [How to build a Raspberry Pi Cluster - SLURM Cluster Config](https://www.youtube.com/watch?v=l5n62HgSQF8)
- [instructions](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3Z2Qkg3V2MwZGxhMUxfc1hBWm9WZGNzMWx4Z3xBQ3Jtc0trbHRxZmxPcTh1eUdXd1RUNEhCM1daWEhPY0JuaHlsUjYwYVJCYldzVkN4aHI5dEFzRmNVZGhtRDZfdHBlN0E4Y0RYNHc4OFlwRUVRc1d6Y2g1OWdHd2xxTGg3ODlaZ0JJSWU1NVRFRE5yZWhKRWozYw&q=https%3A%2F%2Fglmdev.medium.com%2Fbuilding-a-raspberry-pi-cluster-aaa8d1f3d2ca&v=iJnuLnPeoj8)
- [Python Simulations with SLURM](https://www.youtube.com/watch?v=iJnuLnPeoj8)
- [Parallel Computing with Python on a Raspberry Pi Cluster - OpenMPI and mpi4py install](https://www.youtube.com/watch?v=caXD_6JMXfA)
- [Python and SLURM](https://www.youtube.com/watch?app=desktop&v=4lKcou1-3OY)
- [Why would you build a Raspberry Pi Cluster?](https://www.youtube.com/watch?v=8zXG4ySy1m8)
- [blog](https://www.jeffgeerling.com/blog/2021/why-build-raspberry-pi-cluster)
- [I thought Nix is rare in HPC environments but New Mexico State University has it available!](https://hpc.nmsu.edu/discovery/software/nix/)
- [Jeff Geerling's Dramble Raspberry Pi 3 Cluster](https://github.com/geerlingguy/raspberry-pi-dramble)
- [Jeff Geerling Raspberry Pi Cluster Docs](https://github.com/geerlingguy/pi-cluster) [version 1](https://github.com/geerlingguy/turing-pi-cluster)
- [SLURM SBATCH flags](https://slurm.schedmd.com/sbatch.html)
- [SLURM Cheatsheet](https://slurm.schedmd.com/pdfs/summary.pdf)
- [SLURM cgroup.conf reference](https://slurm.schedmd.com/cgroup.conf.html)
- [Someone else's instructions on how to setup SLURM on ubuntu](https://github.com/MagdyA/Slurm-ubuntu-20.04.1)
- [SLURM conf reference](https://slurm.schedmd.com/slurm.conf.html)
- [Introducing HPC with a Raspberry Pi Cluster](https://www.youtube.com/watch?v=HwPUdhu35n4)
- [An interesting deck of slides comparing Kubernetes with SLURM [PDF] (2022)](https://slurm.schedmd.com/SC22/Slurm-and-or-vs-Kubernetes.pdf)
  - SLURM provides better scheduling and job prioritation with granular assignment of specific nodes to have 'features'
  - Kubernetes scales with loads and generally abstracts away where the request goes. Workers can be grouped into pods which is less granular than partitions and node features.
  - SLURM has a fixed set of running nodes on which tasks are assigned, whilst K8s takes and releases nodes as needed
- [SLURM Basic Configuration Usage](https://slurm.schedmd.com/slurm_ug_2011/Basic_Configuration_Usage.pdf)
- [SLURM for Dummies](https://github.com/scottgriffinm/slurm-for-dummies)
- [Dask, a python library to perform data transforms using a compute cluster](https://www.dask.org/get-started)
  - compatible with SLURM and Kubernetes
  - effectively acts as a drop-in replacement for Numpy, Pandas and many other libraries to distribute a particular line of computation to a cluster


### Aside References and inspirations from conferences and lectures
- [An Affordable Supercomputing Testbed based on Raspberry Pi](https://www.youtube.com/watch?v=78H-4KqVvrg)
- [Introduction to HPC -- Andrew Turner (University of Edinburgh](https://www.youtube.com/watch?v=i3cpkJ6iszk)
- [SLURM at NASA](https://www.nccs.nasa.gov/sites/default/docs/tutorials/Intro_Slurm_2020-11.pdf)
  - [Using SLURM -- NASA Center for Climate Simulation](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm)
  - [SLURM Best Practices -- NASA Center for Climate Simulation](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm/best-practices)
  - [Example SLURM scripts](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm/example)
- [FPGA Accelerators at JP Morgan Chase](https://www.youtube.com/watch?v=9NqX1ETADn0) [slides](http://web.stanford.edu/class/ee380/Abstracts/110511-slides.pdf)
- [CFD, PDEs, and HPC: A Thirty-Year Perspective - Paul Fischer, UI-UC](https://www.youtube.com/watch?v=46AwtHqKFb8)
- [GPUs to Mars: Full-Scale simulations of SpaceX's Mars Rocket Engine](https://www.youtube.com/watch?v=vYA0f6R5KAI)
- [Scientific Computing with Intel Xeon Phi Coprocessors](https://www.youtube.com/watch?v=fq_6ckPDNxs)
