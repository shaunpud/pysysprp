from pyinfra.operations import apt, server

apt.packages(
    _sudo=True,
    name="Installing python",
    packages=[
        "build-essential",
        "cargo",
        "pipx",
        "pkg-config",
        "python-is-python3",
        "python3-dev",
        "python3-pip",
        "python3-venv",
    ],
    latest=True,
    update=True,
)

server.shell(
    name="Ensure path pipx",
    commands=[
        "pipx ensurepath",
    ],
)
