import subprocess
import csv
import time

RETRY_SECONDS = 30
MAX_RETRIES = 5


def get_unmounted_volumes():
    process = subprocess.run(["esxcli", "--formatter=csv", "storage", "filesystem", "list"],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    reader = csv.DictReader(
        process.stdout.splitlines(), delimiter=",")

    unmounted = [x.get("VolumeName") for x in reader if x.get(
        "Mounted") == "false" and x.get("Type") == "NFS41"]

    return unmounted


def mount_volume(volume):
    process = subprocess.run(["esxcli", "storage", "filesystem", "mount", "-l", volume],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)


def autostart_vms():
    process = subprocess.run(["vim-cmd", "hostsvc/autostartmanager/autostart"],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)


unmounted = get_unmounted_volumes()
current_retry = 0

while len(unmounted) > 0:
    for volume in unmounted:
        print("Attempting to mount volume '{}'".format(volume))
        mount_volume(volume)

    unmounted = get_unmounted_volumes()
    if len(unmounted) == 0:
        print("Autostarting VMs")
        autostart_vms()
        break

    if current_retry >= MAX_RETRIES:
        print("Maximum number of retries, aborting...")
        break

    current_retry += 1

    print("Some mounts failed, will retry in {} seconds: ".format(
        RETRY_SECONDS, unmounted))
    time.sleep(RETRY_SECONDS)

    unmounted = get_unmounted_volumes()
    if len(unmounted) == 0:
        print("Autostarting VMs")
        autostart_vms()
        break

print("Done!")
