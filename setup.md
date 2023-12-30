[< back](/README.md)
<!--
single piece of hardware could be running multiple operating systems that need
configuring!
-->
# Setup

<details> 
<summary> <b>Table of Contents</b> </summary>
<br/>

<!--toc:start-->
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [OS Configuration and Basic networking setup](#os-configuration-and-basic-networking-setup)
    - [Flashing your microSD cards with Raspberry Pi Imager](#flashing-your-microsd-cards-with-raspberry-pi-imager)
    - [First time SSH Login and IP address of each Node](#first-time-ssh-login-and-ip-address-of-each-node)
    - [Update and upgrade](#update-and-upgrade)
    - [Time Syncing](#time-syncing)
    - [Setting `/etc/hosts` file](#setting-etchosts-file)
    - [Expand Swap (optional)](#expand-swap-optional)
    - [Passwordless SSH between main and worker nodes](#passwordless-ssh-between-main-and-worker-nodes)
        - [Generate ssh key](#generate-ssh-key)
        - [Change password authentication](#change-password-authentication)
        - [Copy public key to target host](#copy-public-key-to-target-host)
  - [Network File System (NFS) setup](#network-file-system-nfs-setup)
        - [Identify the external drive](#identify-the-external-drive)
        - [Format drive](#format-drive)
        - [Create a mount directory](#create-a-mount-directory)
        - [Change permissions on `/clusterfs`](#change-permissions-on-clusterfs)
        - [Get the flash drive's UUID](#get-the-flash-drives-uuid)
        - [Setup automatic mounting of drive](#setup-automatic-mounting-of-drive)
        - [Set loose permissions](#set-loose-permissions)
        - [Export NFS Share](#export-nfs-share)
        - [Mount NFS Share on the worker nodes](#mount-nfs-share-on-the-worker-nodes)
        - [Test the <code>/clusterfs</code> NFS mounts](#test-the-codeclusterfscode-nfs-mounts)
  - [SLURM setup](#slurm-setup)
    - [SLURM Controller on the main node](#slurm-controller-on-the-main-node)
      - [Installing `munge` and `slurm`](#installing-munge-and-slurm)
      - [Configuring `slurm`](#configuring-slurm)
        - [`stow` the config inside `/etc`](#stow-the-config-inside-etc)
    - [SLURM Daemon on the worker nodes](#slurm-daemon-on-the-worker-nodes)
      - [Start munge and slurm services](#start-munge-and-slurm-services)
        - [Enable and run munge](#enable-and-run-munge)
        - [Enable and run slurm daemon](#enable-and-run-slurm-daemon)
        - [Enable and run slurm controller daemon](#enable-and-run-slurm-controller-daemon)
    - [Smoke testing munge](#smoke-testing-munge)
    - [First-time SLURM job submission](#first-time-slurm-job-submission)
  - [Conda (Mamba) setup](#conda-mamba-setup)
  - [Install OpenMPI for each node](#install-openmpi-for-each-node)
  - [Testing the Marzipan Cluster](#testing-the-marzipan-cluster)
<!--toc:end-->

</details>


## Prerequisites
- Install [Raspberry Pi OS imager](https://www.raspberrypi.com/software/) on
  your machine (host) to flash the microSD cards

>:warning: &nbsp; __Note__
>
> Instructions below were tested on __macOS Big Sur__, no effort was taken on
> generalising to Widows or Linux OS. Steps will be similar but some
> details _will_ vary.


## OS Configuration and Basic networking setup
### Flashing your microSD cards with Raspberry Pi Imager

|         field | value                                  |
|           --: | :--                                    |
|        device | `Raspberry Pi 4`                       |
|            OS | `Raspberry Pi OS Lite (64-bit)`        |
|     hostnames | `node01`, `node02`, `node03`, `node04` |
|      username | `admin` as this has root access        |
| user password | different for each node                |
|    enable SSH | `allow public-key authentication only` |

When only allowing public-key authentication, you will need to add your
machine's public RSA key to the Pi to be able to ssh login later.

```bash
# copy the public RSA key of your machine to clipboard
cat ~/.ssh/id_rsa.pub | pbcopy
```

Paste the public RSA key into the `Set authorized_keys for 'admin'` field under
the services tab.

If the commands report no such file or directory, you don't have an RSA key
setup and need to run `ssh-keygen`. This is well documented in the [Raspberry Pi
Foundations
docs](https://www.raspberrypi.com/documentation/computers/remote-access.html#generate-new-ssh-keys).

<details> 
<summary> &nbsp; :pushpin: &nbsp; <h6>Brief on how Passwordless SSH works</h6> </summary>
<br/>

> When enabling SSH with Public-key authentication only, you save your host
> machine's (the one you're using to write the image) public key (ecdsa.pub)
> and the user public key (rsa.pub) into the image. You see the user public key
> in gray in the Raspberry Pi Imager's GUI. When you SSH into the node, you are
> already authorised to enter. The node accepts your machine's request to
> connect gives it's and your host machine exchange their public keys, if not
> done already, to encrypt each other's messages before sending across via the
> network.
> 
> Your host machine may not have its own RSA key, the Raspberry Pi site has
> [docs detailing every step
> here](https://www.raspberrypi.com/documentation/computers/remote-access.html#passwordless-ssh-access).

<!--
 TODO: make the description more accurate:
 - [ref1](https://security.stackexchange.com/questions/20706/what-is-the-difference-between-authorized-keys-and-known-hosts-file-for-ssh/20710#20710)
 - [ref2](https://serverfault.com/questions/690855/check-the-fingerprint-for-the-ecdsa-key-sent-by-the-remote-host)
 - `cat /etc/ssh/ssh_host_ecdsa_key.pub`
-->

</details>


### First time SSH Login and IP address of each Node

```bash
# try login to each node via its hostname
ssh admin@node01.local

# this allows you connect to your node without
# having to know the local ip address it works by
# sending a broadcast to all machines on the network
# to resolve the IP address. It is made possible by
# Avahi and Bonjour (by Apple)

# get the IP address of each node
hostname -I

# or run the following to ssh into each node, and
# echo their IP address and hostname and save it a
# to local file.
ssh admin@node01.local 'echo "$(hostname -I) $(hostname)"' >> node-ip-addr.txt
ssh admin@node02.local 'echo "$(hostname -I) $(hostname)"' >> node-ip-addr.txt
ssh admin@node03.local 'echo "$(hostname -I) $(hostname)"' >> node-ip-addr.txt
ssh admin@node04.local 'echo "$(hostname -I) $(hostname)"' >> node-ip-addr.txt
```

The above assumes there are no two nodes with the same hostname. You can also
use your router/modem's local page to find out the IP address, just make sure
you connect one node at a time to tell them apart.

### Update and upgrade

We will use `apt`, RaspberryOS's package manager, to install new 
software[<sup>^</sup>](https://www.raspberrypi.com/documentation/computers/os.html#using-apt).
It keeps an index of latest available versions of all packages. Let's update
that index and perform an update of any software that's already installed:

```bash
# update apt's source list
sudo apt update

# check all the software awaiting upgrade
apt list --upgradable
# return a count if that's easier
apt list --upgradable | wc -l

# upgrade installed software
sudo apt full-upgrade

# reboot your nodes
sudo reboot
```

Repeat this for all nodes.

### Time Syncing

`munge`'s authentication is based on credentials that expire shortly after
some
time[<sup>^</sup>](https://man.archlinux.org/man/extra/munge/munge.7.en#DETAILS).
So every node must to have its time in sync.
```bash
sudo apt install ntpdate -y

# reboot
sudo reboot
```

### Setting `/etc/hosts` file

It is much easier to refer to a node via its `hostname`, for each node append
the IP addresses of the other nodes with their hostname. Use the
[`node-ip–addr.txt`](#first-time-ssh-login-and-ip-address-of-each-node) from
earlier. When SLURM connects to a node with its `hostname`, the hosts file will
resolve the IP Address.

Example:
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

### Expand Swap (optional)

<details> 
<summary> &nbsp; :warning: &nbsp; <b>It's there to keep the node from freezing</b> </summary>
<br/>

> Swaps are done on the microSD card, none, including the USB sticks can handle
> this kind of I/O–degrades significantly
> [^rpi-se_swap-expansion]. They are also _much_ slower than the internal ram,
> so once this kicks in the process and node generally becomes significantly
> slower to respond. The point of the swap is to prevent the OS from killing
> the `slurmd` causing the SLURM controller to lose all control.

<!--
TODO: setup cgroups or SLURM to kill a job when its exceed a certain amount of
ram. As this expanding swap like this is not a great look.
[An `#SBATCH` flag help help controlling the maximum memory allowed across an entire node](https://slurm.schedmd.com/sbatch.html)
TODO: this swap is huge, do I really need that seeing the node will be down just
from the read/write bottleneck of using swap
TODO: verify if the nodes do indeed not freeze. I think I managed to freeze
them when running the badly designed Geometric Brownian Motion problem.
-->

</details>


```bash
# on each node
sudo vi /etc/dphys-swapfile 

# inside  /etc/dphys-swapfile 
# change to 2GB, actual units MB
CONF_SWAPSIZE=2048

# back in the terminal
# restart dphys-swapfile
/etc/init.d/dphys-swapfile restart

# verify changes
top -n 1 | grep Swap
# should something like this
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   1700.6 avail Mem
```

### Passwordless SSH between main and worker nodes

The `main` nodes must be able to `ssh` into its `workers`. We'll need this later to perform our [`munge` smoke
test](#smoke-testing-munge).

1. on the main node [generate the ssh key](#generate-ssh-key)
2. for each worker node
    1. at worker node, [change password authentication to `yes`](#change-password-authentication)
    2. from main node, [copy the public key to target host](#copy-public-key-to-target-host)
3. afterwards, for each worker node, [change password authentication to `no`](#change-password-authentication)

##### Generate ssh key
```bash
ssh-keygen
```

##### Change password authentication
As you have flashed the nodes to only [accept `public-key authentication
only`](#bootfs-flashing-with-raspberry-pi-imager) you need to temporarily
enable username-password authentication to authorise the client's (`node01`)
public-key`. Make you so disable it afterwards as it makes the node vulnerable
to an unauthorised logins.

[credit](https://serverfault.com/a/684362)

```bash
sudo vi /etc/ssh/sshd_config

# change to yes or no
PasswordAuthentication yes

# restart the ssh daemon
service sshd restart

# double PasswordAuthentication sshd config with
cat /etc/ssh/sshd_config  | grep ^PasswordAuthentication
```

##### Copy public key to target host

```bash
ssh-copy-id <user-in-worker-node>@<worker-node-hostname>
[Enter user password]
```

## Network File System (NFS) setup

When code for the job is [secure copied](https://en.wikipedia.org/wiki/Secure_copy)
to the main node, you want worker nodes to have access to that so they can
perform their part. This also allows results from each worker to placed in one
place.

1. on your main node:
    - [identify the external drive](#identify-the-external-drive)
    - [format the drve to `ext4`](#format-drive)
    - [create the mount directory](#create-a-mount-directory)
        - [change permissions on `/clusterfs`](#change-permissions-on-clusterfs)
        - [get the drive's UUID](#get-the-flash-drives-uuid)
        - [setup automatic mounting of the drive](#setup-automatic-monting-of-drive)
        - [set loose permissions one more time on `/clusterfs`](#set-loose-permissions)
    - [export the NFS Share](#export-nfs-share)
2. for each worker node:
   - [mount the NFS Share on the worker nodes](#mount-nfs-share-on-the-worker-nodes)

##### Identify the external drive
<details>
<summary> &nbsp; :pushpin: &nbsp;  <h6>What is <code>sdal</code>, mounting and <code>sda</code>?</h6> </summary>
<br/>

> Everything is a file, including devices which live inside the `/dev` folder.
> Roughly `sda` refers to storage device 'a', the number following this calleda
> a partition
> [[ref](https://superuser.com/questions/558156/what-does-dev-sda-in-linux-mean)].
> Very generally speaking, 'sd' is usually given to a removable storage device.
> You want to use a removable storage device for the network file system.

</details>

Plug in the USB stick into `node01` which will act at the network file storage

```bash
# run the following command on your main node
lsblk

NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda           8:0    1  3.8G  0 disk               << USB stick
└─sda1        8:1    1  3.8G  0 part /clusterfs    << partition 1
...
```

##### Format drive
```bash
sudo mkfs.ext4 /dev/sda1
```

##### Create a mount directory
```bash
sudo mkdir /clusterfs
```

##### Change permissions on `/clusterfs`

Not exactly a great idea when there are multiple users, but fine for now just
for me
```bash
sudo chown nobody:nogroup -R /clusterfs
sudo chmod 777 -R /clusterfs
```

##### Get the flash drive's UUID

```bash
# get blkid and find 'sda'
blkid /dev/sda*

# get the UUID
/dev/sda1: UUID="5d72d438-90bc-4cd9-9136-d72863c20934"
```

##### Setup automatic mounting of drive

On boot you want the flash drive to be automatically mounted as `/clusterfs`.

```bash
sudo vi /etc/fstab

# append the following with your drive's UUID
UUID=<your-drive-uuid-no-quotes>        /clusterfs      ext4    defaults          0       2

# mount the drive now
sudo mount -a
```

You may need to restart `systemctl daemon-reload` when prompted. Also if the
node throws a `can't find UUID=...` error, [get the flash drive's UUID
again](#get-the-flash-drives-uuid) as it may have changed.

##### Set loose permissions

```bash
sudo chown nobody:nogroup -R /clusterfs
sudo chmod 766 -R /clusterfs/
```

<!--
TODO: explain why 766 not 777
-->

##### Export NFS Share

```bash
sudo apt install nfs-kernel-server -y
sudo vi /etc/exports

# append the following 
/clusterfs <ip-subnet-mask>.0/24(rw,sync,no_root_squash,no_subtree_check)
# example
# if your nodes sit on 192.168.1.XXX then set 192.168.1.0/24
```

<details> 
<summary> &nbsp; :pushpin: &nbsp; <h6>Choosing an <code>ip-subnet-mask</code></h6> </summary>
<br/>

The `/24` means `24` bits are used to define the subnet, and the first
IP address begins at 0, (`192.168.1.0,` `...168.1.1`, etc.) if your IP
address ranges from `192.168.0.0` to `192.168.255.255` then mask as
`192.168.0.0/16` as it takes 16 bits to define `192.168` in binary.

</details>

<details> 
<summary> &nbsp; :pushpin: &nbsp; <h6>NFS Share Export Flags</h6> </summary>
<br/>

|               name | meaning                                                                      |
|                --: | :--                                                                          |
|               `rw` | client has read / write access                                               |
|             `sync` | sync occurs on every transaction                                             |
|    `no-root-squah` | root users on client nodes can write files with root permissions             |
| `no_subtree_check` | prevent errors caused when one node write and another reads at the same time |

</details>

```bash
# update the NFS kernel server
sudo exportfs -a
```

<details> 
<summary> &nbsp; :apple: &nbsp; <h6>Accessing <code>clusterfs</code> from Finder on  macOS</h6> </summary>
<br/>

macOS's NFS mounts creates a port below `1024` as a `non-root` user
which allows the client performs changes to the `node01`'s `clusterfs`
folder as any user. This is obviously insecure.

However the convenience for this exercise is that you can copy and pastes 
across without `scp`. Excluding `insecure` won't make the server invulnerable
to unauthorised entry.

<!--
TODO
I don't think my above xplanation here is accurate
-->

```bash
/clusterfs <ip-address-schema>.0/24(rw,sync,no_root_squash,no_subtree_check, insecure)

# update the NFS kernel server
sudo exportfs -a
```
Security is a big topic, and an NFS server should never be exposed outside of a
trusted network. To read more about `NFS` security
[_here_](https://nfs.sourceforge.net/nfs-howto/ar01s06.html).

</details>



##### Mount NFS Share on the worker nodes

```bash
sudo apt install nfs-common -y
sudo mkdir /clusterfs
sudo chown nobody:nogroup /clusterfs/
sudo chmod -R 777 /clusterfs/

# setup automatic mounting of the nfs share to local /clusterfs
sudo vi /etc/fstab
node01:/clusterfs  /clusterfs   nfs     defaults          0       0

# mount the NFS share
sudo mount -a

# you may need to reload the fstab daemon like so
systemctl daemon-reload
```

##### Test the <code>/clusterfs</code> NFS mounts

```bash
# main node 
# you may need to re-set the permission with chmod/chown
touch /clusterfs/node01-says-hello

# worker nodoes
# check if files available
ls /clusterfs
touch /clusterfs/node02-says-hello

# remove those files, on worker nodes
rm /clusterfs/node*
```


## SLURM setup

We will [setup our `slurm` controller on the main node
(`node01`)](#slurm-controller-on-the-main-node) then 
[setup the worker nodes](#slurm-daemon-on-the-worker-nodes).

### SLURM Controller on the main node

#### Installing `munge` and `slurm`

```bash
# install slurm controller and munge
sudo apt install slurm-wlm -y
```
#### Configuring `slurm`

Use `scp` to copy this repo's `node-config` directory to `/clusterfs`.
```bash
scp -r ./clusterfs/* admin@node01.local:/clusterfs
```

<details> 
<summary> &nbsp; :pushpin: &nbsp; <h6>Brief on what the config contains</h6> </summary>
<br/>

> It contains declarations for each node, the partition of `node01` to
> `node04`, and cluster name: `marzipan` :christmas_tree:.
>
> A cluster of nodes can be members of a group referred to as a
> _Partition_. I have defined two additional partitions apart from
> `all`:
> - `workers`: excludes the `main` node, `node01`.
> - `main`: excludes all `worker` nodes.
>
> Each node has a few _Features_ as well, this depends on physical
> setup, I marked my two to have `high-capacity` (128GB storage),
> `fast` (all cores) for example.
> 
> The `main` node is also constrained to have 2 cores available for SLURM jobs.
> The other 2 cores will handle the Network File Server and the SLURM
> controller. If those services freeze, the entire cluster freezes.
> 

</details>



##### `stow` the config inside `/etc`

The configuration will be shared across all the nodes. You could copy the
config to the correct location for each node, but updating the config quickly
would be error-prone. So we will use `GNU stow` to create a symbolic link.
This way we have one copy and accessible in all the right places. After each
restart all your nodes, making sure the `main` node is rebooted last.

```bash
# install stow
sudo apt install stow

# go to our config
cd /clusterfs/node-config

# Remove empty environment file
sudo rm /etc/environment

# stow slurm config
sudo stow etc/ -t /etc

# check if successful
ls -lah /etc/slurm

# files that are symbolic links appears like below
slurm.conf -> ../../clusterfs/node-config/etc/slurm/slurm.conf

# reboot
sudo reboot
```
Copy the main node's munge key to `/clusterfs` for sharing

```bash
# copy the munge key to be shared with worker nodes
mkdir /clusterfs/node-config/.secrets/munge
sudo cp /etc/munge/munge.key /clusterfs/node-config/.secrets/munge
```

The `node-config/etc` also contains the file `environment` which contains a
single environment variable `CLUSTER_ENVS`. We will use this later to create,
and refer to shared `micromamba` / `conda` environments between jobs. Any
environment variable inside the `environment` file will be available to
interactive/non-interactive shells and processes such as `sbatch`.

<!--
TODO: keeping this environment variable inside the `environment` file is a
fairly large scope. Is there a way to reduce the scope? Does `sbatch` really
need it?
-->

<details> 
<summary> &nbsp; :lemon: &nbsp; <h6>If you want a fresh config follow this</h6> </summary>

```bash
# copy, extract and name config to /etc/slurm
cd /etc/slurm
cp /usr/share/doc/slurm-client/examples/slurm.conf.simple.gz .
sudo cp /usr/share/doc/slurm-client/examples/slurm.conf.simple.gz .
sudo gzip -d slurm.conf.simple.gz 
sudo mv slurm.conf.simple slurm.conf
```
</details>


### SLURM Daemon on the worker nodes

```bash
# install SLURM Client
sudo apt install slurmd slurm-client -y
```

Then [`stow` the slurm config like in the main node](#stow-the-config-inside-etcslurm).

Copy `node01`'s `munge.key` to the right place in each worker node. This will
enable all nodes to encrypt and decrypt each other's messages.
```bash
sudo cp /clusterfs/node-config/.secrets/munge/munge.key \
        /etc/munge/munge.key
```

<details> 
<summary> &nbsp; :question: &nbsp; <h6>Why can't we symbolically link the <code>munge.key</code></h6> </summary>
<br/>

> The `munge.key` is the used by the nodes to encrypt and decrypt each other's
> messages. For security reasons, `munge` will not follow a symbolic link. We
> can do better and ensure only `munge` has permissions to read and write,
> but this has been omitted.

</details>


#### Start munge and slurm services

1. [Enable munge](#enable-and-run-munge), 
   [slurm daemon](#enable-and-run-slurm-daemon) and 
   [slurm controller daemon](#enable-and-run-slurm-controller-daemon)
   on the main node.
2. Then, [enable munge](#enable-and-run-munge) and 
   [slurm daemon](#enable-and-run-slurm-daemon) on the worker nodes.

##### Enable and run munge

```bash
sudo systemctl enable munge
sudo systemctl start munge
```

##### Enable and run slurm daemon
```bash
sudo systemctl start slurmd
sudo systemctl enable slurmd
```
##### Enable and run slurm controller daemon
```bash
# main node only!
sudo systemctl enable slurmctld
sudo systemctl start slurmctld
```


### Smoke testing munge

Please note you need to have [setup passwordless SSH between main and
workers](#passwordless-ssh-between-main-and-worker-nodes).

Here we check if something munged in `node02` can be unmunged by `node01`:
```bash
# from node01, ssh into nodes02-04, example below
ssh admin@node02 munge -n | unmunge | grep STATUS

# expected result like
Success (0)

# if there is a credential error
# reboot your main and worker nodes
# then try again
sudo reboot
```


### First-time SLURM job submission
>

__Check your nodes on your main node with `sinfo`__
```bash
# from you host machine
ssh admin@node01.local sinfo

# expected output
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
main         up   infinite      1   idle node01
workers      up   infinite      3   idle node[02-04]
all*         up   infinite      4   idle node[01-04]
```

__Smoke test job__
```bash
# let's get the hostname for each node in the partition
srun --nodes=4 hostname
# each nodes echo's its hostname
```
<details> 
<summary> &nbsp; :white_check_mark: &nbsp; <b>More tests, tiny tour of SLURM</b> </summary>
<br/>

> SLURM is incredibly good at scheduling: when, what nodes, for long, at what
> priority. Below are some test that demonstrate the `slurm.conf` implemented.

```bash

# try targeting specific partitions
srun -p main -N 1 hostname
srun -p workers -N 3 hostname
srun -p all -N 4 hostname

# notice SLURM schedules jobs on worker _before_ main

# only workers assigned
srun -p all -N 1 hostname
srun -p all -N 2 hostname
srun -p all -N 3 hostname

# this submits 4 jobs so the main gets to work
srun -p all -N 4 hostname

# you can target by constraint
# the constraints are 'Features' defined in slurm.conf
# to setup to reflect my nodes
srun -C main -N 1 hostname
srun -C fast,high-capacity -N 2 hostname
srun -C fast -N 3 hostname

# main is constrained to only allow 2 jobs
# that's 1 job per core, the 2/4 cores are reserved for SLURM and NFS
# notce SLURM cannot assign more than two jobs
srun -C main -n 2 hostname
srun -C main -n 3 hostname
```

</details>


## Conda (Mamba) setup

Conda is a versatile package manager for installing complex polygot
packages, it is widely used in the data, scientific and finance communities.
However it is a little heavy, so I have opted for `micromamba` which is a single
statically linked binary. There is `miniconda`, but so far I have had a good
time with `micromamba`.

See [micromamba installation page](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).

You can examine the [script _here_](https://raw.githubusercontent.com/mamba-org/micromamba-releases/main/install.sh).

Install `micromamba`:
```bash 
srun -p all --nodes 4 bash -c \
'"${SHELL}" <(curl -L micro.mamba.pm/install.sh)'

# the script is interactive when installed with a
# terminal is attached, otherwise will quietly
# install as intended here

# check micromamba version on each node
srun -p all --nodes 4 bash -c \
'echo "$(hostname) $(sudo ~/.local/bin/micromamba --version)"'

# each node should report the version of micromamba

# if there is an issue, restart the nodes
# lets the workers take the lead
srun -p workers -N 3 sudo reboot
# restart main node
sudo reboot
```

<!--
TODO: Figure out how to correctly cancel all jobs, restart or shutdown nodes,
with the correct order. Currently, when the worker nodes shutdown, the `STATUS`
of the nodes is not updates. Technically the status should be updated immediate
after the shutdown signal has been received to prevent them from taking on new
jobs.
-->


## Install OpenMPI for each node

```bash
# enter super user mode
sudo su -

# submit job to install OpenMPI packages on all nodes
srun --nodes=4 apt install \
                   openmpi-bin \
                   openmpi-common \
                   libopenmpi3 \
                   libopenmpi-dev \
                   -y


# restart your nodes
```

<!--
TODO: What am I trading off when not compiling the binary myself?
[OpenMPI docs suggests compiling, configuring and make install yourself](https://docs.open-mpi.org/en/main/installing-open-mpi/quickstart.html)

TODO: Why does this _need_ super user mode?

TODO: How do these contribute to the OpenMPI functionality? Why isn't there a daemon
that needs enabling & and starting?
-->


## Testing the Marzipan Cluster

```bash
cd /clusterfs/jobs/mpi-hello-c
sbatch SUB

cd /clusterfs/jobs/micromamba-activate
sbatch SUB

# in each expect a new result.out file
# it should be clear it is free of errors
```
