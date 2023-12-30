## On start up, some or all my nodes shown as `DOWN*`
- unable to reproduce this problem but here are some pointers:
- rebooting the `DOWN`ed nodes brings them back to `idle` state
- my hunch is that there is a race condition between the main and the worker
  nodes, which leads to some looking like they are down, the only problem with
  this hunch is that the worker nodes once healthy and idle should be reporting
  back to the main node. So I should still expect them to be updated to the
  correct state.
- [Raspberry Pi Forum reported this, but only after reboot](https://forums.raspberrypi.com/viewtopic.php?t=252185)
- [SLURM troubleshooting page on debugging `DOWN` state nodes](https://slurm.schedmd.com/troubleshoot.html#nodes)

## The usb stick is unreadable on my mac, is the format wrong?
   > uses `ext4` which the mac cannot read, try formatting with a different
   > filesystem format that still works with `nfs`
   > the SD cards are flashed with FAT32 but that it only allows maximum
   > file sizes of 4GB

## figure out how to sync files between master and my mac: secure copy, rsync, syncthing?
   > `scp` is very nice when passwordless ssh is setup

## run the workloads only on node 2 to see if freezing happens then
   > freezing happens because of job overflowing in memory triggering the killing
   > of `slurmd` sub-processes. It leaves the node in a bad unresponsive state
   > as the memory is still not freed (potentially a `cgroup.conf` issue)

## Can I change `mkfs.ext4` to `mkfs.exfat`, so both linux and macOS can read the usb drive?
  > ext4 is not compatible with macOS without some file system daemon
  > FAT32 is most promising but file can't be larger than 4GB
  > ExFAT is a proprietary format by Microsoft so more software needed
  > current `scp` is best
