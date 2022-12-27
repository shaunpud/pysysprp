from pyinfra.operations import apt

apt.update(
    _sudo=True,
    name="Updating repository",
)

apt.dist_upgrade(
    _sudo=True,
    name="Upgrading packages",
)
