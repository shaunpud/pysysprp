from pyinfra.operations import apt

apt.packages(
    _sudo=True,
    name="Installing nginx",
    packages=[
        "apache2-utils",
        "nginx",
    ],
    latest=True,
    update=True,
)
