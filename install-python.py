from pyinfra.operations import apt

apt.packages(
    _sudo=True,
    name="Installing python",
    packages=[
        "build-essential",
        "pipx",
        "python3-dev",
        "python3-pip",
        "python3-venv",
    ],
    latest=True,
    update=True,
)
