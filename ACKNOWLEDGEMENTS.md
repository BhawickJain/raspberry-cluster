# Acknowledgements

The setup is hugely inspired by [Garrett Mill's
Guide](https://garrettmills.dev/blog/2019/04/29/Building-a-Raspberry-Pi-Cluster-Part-I).
I have to made a few improvements to the configuration namely the use of `stow`
for shared SLURM configuration, using secure copy `scp`, extending smoke tests
and finally `micromamba` for codifying and sharing shell environments for
each job.

The following have my gratitude and learned a great deal:

- [This Stackoverflow user gave me the brainwave I needed to correctly `export` environment variables](https://stackoverflow.com/questions/65960509/slurm-error-when-submitting-to-multiple-nodes-slurmstepd-error-execve-py)
- [Garrett Mill's Guide on creating a Raspberry Pi Cluster](https://garrettmills.dev/blog/2019/04/29/Building-a-Raspberry-Pi-Cluster-Part-I/)
- [Wes Kendall's `helloworld.c` which help me debug and verify the OpenMPI installation](https://mpitutorial.com/tutorials/mpi-hello-world/)
- [Team behind `mamba` for amazing package manager](https://mamba.readthedocs.io/en/latest/index.html)
