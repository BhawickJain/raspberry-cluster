#!/bin/bash

set -x

# shutdown main node last
sudo shutdown -h +2

# shutdown worker nodes
srun -p workers -N 3 bash -c 'sudo shutdown -h +1'
