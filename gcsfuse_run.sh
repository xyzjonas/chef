#!/usr/bin/env bash
set -eo pipefail

# https://cloud.google.com/run/docs/tutorials/network-filesystems-fuse#cloudrun_fs_script-python
# Create mount directory for service
echo "Mounting GCS Fuse at $MNT_DIR"
mkdir -p $MNT_DIR
# Use implicit dirs created directories before FUSE mounts the bucket...
gcsfuse --debug_gcs --debug_fuse --implicit-dirs $BUCKET $MNT_DIR
echo "Mounting completed."

exec chef &

# Exit immediately when one of the background processes terminate.
wait -n