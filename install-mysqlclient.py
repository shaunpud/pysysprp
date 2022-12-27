from pyinfra.operations import apt

apt.packages(
    _sudo=True,
    name="Installing mysql client/dev",
    packages=[
        "default-libmysqlclient-dev",
        "default-mysql-client",
    ],
    latest=True,
    update=True,
)
