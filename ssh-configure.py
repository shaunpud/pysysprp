from io import StringIO
from pyinfra.operations import files, server

sshport = input("\nSSH Port: ")
if not sshport or int(sshport) < 1 or int(sshport) > 65535:
    exit("Invalid SSH Port")

files.put(
    _sudo=True,
    name="Creating ssh config",
    src=StringIO(
        f"""AddressFamily inet
Port {sshport}
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes"""
    ),
    dest="/etc/ssh/sshd_config.d/99-custom.conf",
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
    _env={
        "DEBIAN_FRONTEND": "noninteractive",
    },
)

files.put(
    _sudo=True,
    name="Hardening as per sshaudit.com",
    src=StringIO(
        f"""KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,gss-curve25519-sha256-,diffie-hellman-group16-sha512,gss-group16-sha512-,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-256-cert-v01@openssh.com"""
    ),
    dest="/etc/ssh/sshd_config.d/98-hardening.conf",
    mode=600,
)

server.service(
    _sudo=True,
    name="Reloading ssh service",
    service="ssh",
    reloaded=True,
)
