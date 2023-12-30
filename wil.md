# What I learned

Here are some unstructured notes I have made, overtime I will place into a document with reasonable context.
- SLURM has been incredibly slick to use and setup.
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
- if you can run sudo you have root privileges
 if you run more tasks than there are cores it will wait indefinitely for a
  partition to have enough resources
  - for example, `srun --ntasks=8 hostname` is fine on my two node setup, but
    `srun --ntasks=9 hostname` is not
- the master is not a compute node as if it dies its blocks the workers
- performing a large geometric brownian motion continuously needed a whole load
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
    have multiple nodes generate them if need be [see parallel
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
- you can target specific set of nodes with ranges, and exclude nodes
  - `--nodelist / -w` 
  - `--exclude / -x`
  - TODO: try targeting multiple nodes with this
  - [docs](https://slurm.schedmd.com/srun.html)

## References
- [^se_local]: [What does ".local" do? -- Ubuntu Stack Exchange](https://askubuntu.com/questions/4434/what-does-local-do)
- [^se_turn-off-pi]: [How do I turn off my raspberry pi -- Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/a/383)
