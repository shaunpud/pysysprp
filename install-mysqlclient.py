from pyinfra.operations import apt

apt.packages(
    _sudo=True,
    name="Installing mysql client/dev",
    packages=[
        "default-libmysqlclient-dev",
        "mariadb-backup",
    ],
    latest=True,
    update=True,
)
