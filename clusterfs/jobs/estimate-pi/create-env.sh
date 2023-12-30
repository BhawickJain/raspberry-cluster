#!/bin bash

set -eu

ENV='python-numpy-mpi4py'

JOB_ENV_PATH="$CLUSTER_ENVS/$ENV"

if [ ! -d "$CLUSTER_ENVS" ]; then
	mkdir "$CLUSTER_ENVS"
fi

micromamba create -f env.yaml -p "$JOB_ENV_PATH" -y

