from pyinfra.operations import apt

apt.packages(
    _sudo=True,
    name="Installing utilities",
    packages=[
        "curl",
        "dnsutils",
        "git",
        "htop",
        "iptables",
        "jq",
        "lftp",
        "lsb-release",
        "lsof",
        "pigz",
        "pwgen",
        "rsync",
        "screen",
        "sudo",
        "telnet",
        "unzip",
        "wget",
        "whois",
        "zip",
    ],
    latest=True,
    update=True,
)
