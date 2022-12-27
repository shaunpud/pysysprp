from pyinfra.operations import apt, server

apt.packages(
    _sudo=True,
    name="Installing python",
    packages=[
        "build-essential",
        "python3-dev",
        "python3-pip",
        "python3-venv",
    ],
    latest=True,
    update=True,
)

server.shell(
    _sudo=True,
    name="Updating pip",
    commands=[
        "pip3 install --upgrade pip",
    ],
)
