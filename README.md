# esxi-nfs-automounter.py

If your NFS datastore is unavailable when VMware ESXi boots, it stays unmounted until you manually mount it or reboot the host. This also prevents any VM residing on this datastore from starting. This script will repeatedly attempt to mount all unmounted NFS41 volumes and once all volumes are mounted it will execute the VM autostart process.

## Installation

Copy the `esxi-nfs-automounter.py` script to a datastore on your ESXi host.  Don't copy it to a datastore that might not mount on boot (e.g. an NFS datastore).

Modify your `/etc/rc.local.d/local.sh` and add `python3 /vmfs/volumes/[datastore]/esxi-nfs-automounter.py` to the end of the file right above `exit 0`. 

Replace "[datastore]" with the location you copied the script.

Example local.sh:

```
#!/bin/sh

# local configuration options

# Note: modify at your own risk!  If you do/use anything in this
# script that is not part of a stable API (relying on files to be in
# specific places, specific tools, specific output, etc) there is a
# possibility you will end up with a broken system after patching or
# upgrading.  Changes are not supported unless under direction of
# VMware support.

# Note: This script will not be run when UEFI secure boot is enabled.

python3 /vmfs/volumes/datastore1/esxi-nfs-automounter.py

exit 0
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)