# Raspberry Pi Super Computer Cluster

- [ ] Motivation?
  - [Why would you build a Raspberry Pi Cluster?](https://www.youtube.com/watch?v=8zXG4ySy1m8)
  - [blog](https://www.jeffgeerling.com/blog/2021/why-build-raspberry-pi-cluster)

- [ ] use HPC job management software like SLURM
  - [Parallel Computing with Python on a Raspberry Pi Cluster - OpenMPI and mpi4py install](https://www.youtube.com/watch?v=caXD_6JMXfA)
  - [Python Simulations with SLURM](https://www.youtube.com/watch?v=iJnuLnPeoj8)
- [ ] host a site or a service that performs a service much cheaper than a cloud service
- [ ] perform parallelised math problem jobs
- [ ] manage a NAS drive
- [ ] isolated linux computer, it won't matter if I break it
- [ ] node clusters to serve a function

- [ ] Is this a super computer or a just a compute cluster?

- [Python and SLURM](https://www.youtube.com/watch?app=desktop&v=4lKcou1-3OY)

## Build Plan

- [ ] create a build plan to make it certain how exactly you will build and use it.
- [Raspberry Pi Cluster Ep 1 - Introduction to Clustering](https://www.youtube.com/watch?v=kgVz4-SEhbE)
- [How to build a Raspberry Pi Cluster - SLURM Cluster Config](https://www.youtube.com/watch?v=l5n62HgSQF8)
- [instructions](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa3Z2Qkg3V2MwZGxhMUxfc1hBWm9WZGNzMWx4Z3xBQ3Jtc0trbHRxZmxPcTh1eUdXd1RUNEhCM1daWEhPY0JuaHlsUjYwYVJCYldzVkN4aHI5dEFzRmNVZGhtRDZfdHBlN0E4Y0RYNHc4OFlwRUVRc1d6Y2g1OWdHd2xxTGg3ODlaZ0JJSWU1NVRFRE5yZWhKRWozYw&q=https%3A%2F%2Fglmdev.medium.com%2Fbuilding-a-raspberry-pi-cluster-aaa8d1f3d2ca&v=iJnuLnPeoj8)
- Gareth Mills articles: 
  - [Part I](https://glmdev.medium.com/building-a-raspberry-pi-cluster-784f0df9afbd)
  - [Part II](https://glmdev.medium.com/building-a-raspberry-pi-cluster-aaa8d1f3d2ca)
  - [Part III](https://glmdev.medium.com/building-a-raspberry-pi-cluster-f5f2446702e8)

### Parts

- [raspberry pi 4 model b, 2gb](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/): ideally 4 gb but its double the price, ideally Pi 5 but that's astronomical for current project scope
- [poe hat](https://www.raspberrypi.com/products/poe-hat/): enables pi's to be powered via ethernet, significantly reducing material and clutter with a minor penality on clock speed (1.5GHz instead of 1.8GHz) `[ref needed]`
  - [additional details](https://www.raspberrypi.com/news/announcing-the-raspberry-pi-poe-hat/)

### Assembly

### Software Setup
  - [Raspbery Pi OS](https://www.raspberrypi.com/software/)  
  - [Etcher](https://etcher.balena.io/#download-etcher)

### What I learned
 - when setting `nobody.nogroup`, set `nobody:nogroup` instead
 - when setting an ip range is it always 192.168.Y.0/24, where Y is a subnet on
   my network its 5 but is usually 1. 
 - passwordless SSH is might easier than I had imagined
   - each machine needs to have an RSA key ready. You place exachange the
     RSA.pub and it is set as a line on `~/.ssh/authorised_keys`
   - when the user machine connects to the remote machine, the username you
     write determines which `authorised_keys` is checked
   - if the RSA.pub matches the entry in the remote machine's user then it will
     connect, if not it is not authorised
   - during the raspberry pi bootfs flashing you setup the user machine's
     RSA.pub under a default user you've created
 - you can connect to a remote machine that is in the Local Area Network with
   `<hostname>.local` which sends a broadcast to all machines to reply if their
   hostname matches the call [^se_local]. This is nice and easy, though it is
   best and safer if you map the remote machine hostname with the IP address in
   the hosts file of your local machine.
 - you can safely shutdown your nodes with the `sudo shutdown -h now` command
   [^se_turn-off-pi].
   - be sure to send the shutdown signal to main node last (i.e. node01)
   - this ensures NFS server does not disappear on the follow nodes leading
     them to wait until timeout
 - if you can run sudo you have root priveleges
- if you run more tasks than there are cores it will wait indefinitely for a
  partition to have enough resources
  - for example, `srun --ntasks=8 hostname` is fine on my two node setup, but
    `srun --ntasks=9 hostname` is not
- the master is not a compute node as if it dies its blocks the workers
- performing a large geometric brownian motion continously needed a whole load
  of RAM, even on my local machine
  - the bottleneck is having to generate and keep 4Million random samples in
    memory which is not great 
  - the space complexity is O(n)
  - even if my local machine is faster, it still takes 9 seconds per million
    samples, with 3 rpi nodes, I can do generate that in 6 seconds
- ensure master node is not a compute node makes thing far more controllable
- the reason my PI's freeze and die is because of memory overflow, adding swap
  ensured pi doesn't freeze but instead slows down
- running 1Billion samples takes approximates 8GB of ram which is obviously the
  wrong approach
  - if I really want to make large samples, I need to store them on disk and
    have mutiple nodes generate them if need be [see parallel
    generation](https://numpy.org/doc/stable/reference/random/index.html#parallel-generation)
- when monitoring the node state and queue the following are useful
  - `squeue -i5` output queue state every 5 seconds
  - `sinfo -i5` output partition state every 5 seconds
- secure copy recipes
  - `scp -r bhawick@node01.local:/clusterfs/some-dir problems/some-other-dir`
- copy the content of a file into clipboard without `scp`
  - `ssh bhawick@node01.local cat /clusterfs/some-file | pbcopy`
  - you can pipe into a file or something else!
- SLURM main node does not need to have passwordless SSH setup inorder for
  Munge to work
  - instead this is there to perform a manual check via SSH to munge/unmunge
  - since SSH is setup as Passwordless, password auth is disabled
  - so it is a matter of convenience and sanity checking
- `uptime` command gives you how long the unix system has been running since
  last startup

### TODO
- [x] ensure master is not part of the compute cluster
- [ ] usb stick is unreadable on my mac, is the format wrong?
      > uses `ext4` which the mac cannot read, try formatting with a different
      > filesystem format that still works with `nfs`
- [x] figure out how to sync files between master and my mac: secure copy, rsync, syncthing, 
      > `scp` is very niec when passwordless ssh is setup
- [x] run the workloads only on node 2 to see if freezing happens then
      > freezing happens because of job overflowig in memory triggering the killing
      > of `slurmd` sub-processes. It leaves the node in a bad unresponsive state
      > as the memory is still not freed (potentially a `cgroup.conf` issue)

### References
- [Jeff Geerling's Dramble Raspberry Pi 3 Cluster](https://github.com/geerlingguy/raspberry-pi-dramble)
- [Jeff Geerling Raspberry Pi Cluster Docs](https://github.com/geerlingguy/pi-cluster) [version 1](https://github.com/geerlingguy/turing-pi-cluster)
- [Power Over Ethernet (PoE and PoE+)](https://www.youtube.com/watch?v=dVq9jHwmCrY)
  - Power Source Equipment (PSE) like a PoE switch
  - you can use a PoE injector
  - PoE (203) 12.95W and PoE+ (25.5W), PoE+ backwards compatible
- [Raspberry Pi's new PoE+ HAT](https://www.youtube.com/watch?v=XZ08QKAbBoU)
  - recommends sticking with the original PoE Hat as the new one has more power
    draw without immediate benefits for server/compute node architectures
  - [Raspberry Pi PoE+ HAT - eBay](https://www.ebay.co.uk/itm/134181695050?hash=item1f3dda2e4a:g:ubsAAOSw1pdi3pYf&amdata=enc%3AAQAIAAAA8BE76UfPjtzXWUEOBv3vMEXDERnkeGJAgFpH%2BSzkGCQrqPoZLX1lzORkKIzm6Qci5Gt8cgw0dQ1EYq0vkl3EyZ%2FADEvChIapOSGC730XMdUjn8T6Q8A5eNCUlXqT3%2BfW5lwsRKuq2kGQozBwCEJwVJbZY0odkmrVUIZ9JNyEjn33G4PRZ7ku%2BYut4BJIhleqC2yGglLK6q6ova0HosCxfF%2B7XAjkfa9cs8q3B56yfcJplBUwCSD2%2FCIsQEGs4hJmw5hn9tDrR4MauAmsgaCA3uoyuIshAmmTrkMj%2B1TwSb%2B2Qj3uB5IJGqsydj5HYDTj%2Bw%3D%3D%7Ctkp%3ABk9SR9jshsKBYw)
  - it is slightly bigger which means it might not fit a Pi Case or slide into a rack as easily
  - Basically if you run into a problems with the orignal PoE hat _then_ buy it.
- [SLURM at NASA](https://www.nccs.nasa.gov/sites/default/docs/tutorials/Intro_Slurm_2020-11.pdf)
  - [Using SLURM -- NASA Center for Climate Simulation](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm)
  - [SLURM Best Practices -- NASA Center for Climate Simulation](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm/best-practices)
  - [Example SLURM scripts](https://www.nccs.nasa.gov/nccs-users/instructional/using-slurm/example)
- [SLURM SBATCH flags](https://slurm.schedmd.com/sbatch.html)
- [SLURM Cheatsheet](https://slurm.schedmd.com/pdfs/summary.pdf)
- [SLURM cgroup.conf reference](https://slurm.schedmd.com/cgroup.conf.html)
- [Someone else's instructions on how to setup SLURM on ubuntu](https://github.com/MagdyA/Slurm-ubuntu-20.04.1)
- [SLURM conf reference](https://slurm.schedmd.com/slurm.conf.html)

### Aside References and inspirations from conferences and lectures
- [FPGA Accelerators at JP Morgan Chase](https://www.youtube.com/watch?v=9NqX1ETADn0) [slides](http://web.stanford.edu/class/ee380/Abstracts/110511-slides.pdf)
- [CFD, PDEs, and HPC: A Thirty-Year Perspective - Paul Fischer, UI-UC](https://www.youtube.com/watch?v=46AwtHqKFb8)
- [GPUs to Mars: Full-Scale simulations of SpaceX's Mars Rocket Engine](https://www.youtube.com/watch?v=vYA0f6R5KAI)
- [An Affordable Supercomputing Testbed based on Rasberyy Pi](https://www.youtube.com/watch?v=78H-4KqVvrg)
- [Scientific Computing with Intel Xeon Phi Coprocessors](https://www.youtube.com/watch?v=fq_6ckPDNxs)
- [Introduction to HPC -- Andrew Turner (University of Edinburgh](https://www.youtube.com/watch?v=i3cpkJ6iszk)


### Footnotes
- [^se_local]: [What does ".local" do? -- Ubuntu Stack Exchange](https://askubuntu.com/questions/4434/what-does-local-do)
- [^rpi-docs_passwordless-ssh]: [Passwordless SSH Access -- Raspberry Pi Docs](https://www.raspberrypi.com/documentation/computers/remote-access.html#passwordless-ssh-access)
- [^se_turn-off-pi]: [How do I turn off my raspberry pi -- Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/a/383)
