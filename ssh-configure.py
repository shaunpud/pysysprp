from io import StringIO
from pyinfra.operations import files, server

sshport = input("\nSSH Port: ")
if not sshport or int(sshport) < 1 or int(sshport) > 65535:
    exit("Invalid SSH Port")

files.put(
    _sudo=True,
    name="Creating ssh config",
    src=StringIO(f"""Port {sshport}
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes"""),
    dest="/etc/ssh/sshd_config.d/custom.conf",
    mode=600,
)

server.shell(
    _sudo=True,
    name="Removing ssh keys",
    commands=[
        "rm -f /etc/ssh/ssh_host*",
    ],
)

server.shell(
    _sudo=True,
    name="Generating ssh keys",
    commands=[
        "dpkg-reconfigure openssh-server",
    ],
)

server.service(
    _sudo=True,
    name="Reloading ssh service",
    service="ssh",
    reloaded=True,
)
