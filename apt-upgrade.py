import sys

from pyinfra.operations import apt, server

reboot = input("\nReboot? [y/N] ")

apt.update(
    _sudo=True,
    name="Updating repository",
)

apt.dist_upgrade(
    _sudo=True,
    name="Upgrading packages",
)

if reboot.lower().strip() == "y":
    server.reboot(
        _sudo=True,
        name="Rebooting",
    )
