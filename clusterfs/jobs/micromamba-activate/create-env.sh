#!/bin bash

set -eu

ENVIRONMENT='python-mpi4py'

SHARED_ENVIRONMENTS_DIR='../../environments'
JOB_MAMBA_PREFIX="$SHARED_ENVIRONMENTS_DIR/$ENVIRONMENT"

if [ ! -d "$SHARED_ENVIRONMENTS_DIR" ]; then
	mkdir "$SHARED_ENVIRONMENTS_DIR"
fi

micromamba create -f env.yaml -p "$JOB_MAMBA_PREFIX" -y

