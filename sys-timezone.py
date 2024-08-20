from io import StringIO
from pyinfra.operations import files, server

files.put(
    _sudo=True,
    name="Creating timezone file",
    src=StringIO("Australia/Perth"),
    dest="/etc/timezone",
)

server.shell(
    _sudo=True,
    name="Setting timezone",
    commands=[
        "timedatectl set-timezone Australia/Perth",
    ],
)

server.shell(
    _sudo=True,
    name="Setting lang",
    commands=[
        "localectl set-locale LANG=C.UTF-8",
    ],
)
