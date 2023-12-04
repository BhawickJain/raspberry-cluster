## bootfs flashing

### passwordless key-based ssh



### setting /etc/hosts file

For each node map the IP Address of other sibling nodes in the hosts files,
here are two examples:

```bash
# @node 01 /etc/hosts
127.0.1.1   node01
<ip addr>   node02
# .. more sibling nodes

# @node 02 /etc/hosts
127.0.1.1   node02
<ip addr>   node01
# .. more sibling nodes
```

### expand swap

> :warning: &nbsp; __It's there to keep the node from freezing__
> 
> Swaps are done on the microSD card, none, including the USB sticks can handle
> this kind of I/O---their lifespan degrades significantly
> [^rpi-se_swap-expansion]. They are also _much_ slower than the internal ram,
> so once this kicks in the process and node generally becomes significantly
> slower to respond. The point of the swap is to prevent the OS from killing
> the `slurmd` causing the slurm controller to lose control. 

```bash
# on each node
sudo vi /etc/dphys-swapfile 

## /etc/dphys-swapfile 
# change to 2GB, actual units MB
CONF_SWAPSIZE=2048

# back in the terminal
# restart dphys-swapfile
/etc/init.d/dphys-swapfile restart

# check on top
top -n 1 | grep Swap
# should somethig like this
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   1700.6 avail Mem
```

### setup passwordless SSH between main and workers

__generate ssh key__
```bash
ssh-keygen
```

__change password authencation__
[credit](https://serverfault.com/a/684362)
```bash
sudo vi /etc/ssh/sshd_config

# change to yes or no
PasswordAuthentication yes

# restart the ssh daemon
service sshd restart

# double PasswordAuthentication sshd config with
cat /etc/ssh/sshd_config  | grep ^PasswordAuthentication
```

__copy public key to target host__
```bash
ssh-copy-id <user-in-worker-node>@<worker-node-hostname>
[Enter user password]
```

1. on the main node generate the ssh key
2. for each worker node
   1. at worker node, change password authentication to yes
   2. from main node, copy the public key to target host
   3. at worker node, change password authentication to no


## setup network file system


## setup munge and slurm

### install slurm

```bash
sudo apt install slurm-wlm -y
```

Install slurm on main and workers nodes. This installs both slurm daemon, slurm
controller daemon and munge. Munge is how the controller on main communicates
to the worker nodes.

### copy .conf to workers

<detail> 
<summary> &nbsp; __if you want a fresh config follow this__ </summary>
```bash
# copy, extract and name config to /etc/slurm
cd /etc/slurm
cp /usr/share/doc/slurm-client/examples/slurm.conf.simple.gz .
sudo cp /usr/share/doc/slurm-client/examples/slurm.conf.simple.gz .
sudo gzip -d slurm.conf.simple.gz 
sudo mv slurm.conf.simple slurm.conf
```
</detail>


```bash
# copy munge key to worker to be able to unmunge messages
sudo cp /clusterfs/munge.key /etc/munge/munge.key

# copy all slurm configs to worker slurm
sudo cp /clusterfs/slurm.conf /etc/slurm/slurm.conf
sudo cp /clusterfs/cgroup* /etc/slurm/

```

Search nod01/02/... and change their ip addr

### start munge and slurm services

__Enable and run munge__

```bash
sudo systemctl enable munge
sudo systemctl start munge
```
__Enable and run slurm daemon__
```bash
sudo systemctl start slurmd
sudo systemctl enable slurmd
```
__Enable and run slurm controller daemon__
```bash
sudo systemctl enable slurmctld
sudo systemctl start slurmctld
```

Enable munge, slurm daemon and slurm controller daemon on the main node.
Then, enable munge and slurm daemon on the worker nodes.

### test munge

Please note you need to have setup passwordless SSH between main and workers.

__something munged in node02 can be unmunged by node01__
```bash
ssh <uname>@<node02-ip-address> munge -n | unmunge | grep STATUS

# expected result like
Success (0)
```

__reboot all nodes if necessary__
Ensure main node is last as the `nfs` daemon will have to timeout leading to an
awkward wait
```bash
sudo reboot
```

