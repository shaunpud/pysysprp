import json
import os
import random
import re

from io import StringIO
from pyinfra.operations import apt, files, server
from urllib.request import urlopen

administrator = input("\nAdministrator: ")
if not administrator or not re.match(r"^[a-z0-9-_]+$", administrator, flags=re.I):
    exit("Invalid Username")

agentsdata = "https://raw.githubusercontent.com/EIGHTFINITE/top-user-agents/main/index.json"
useragents = json.loads(urlopen(agentsdata).read().decode())

apt.packages(
    _sudo=True,
    name="Installing sudo",
    packages=[
        "sudo",
    ],
    latest=True,
    update=True,
)

server.user(
    _sudo=True,
    name=f"Creating {administrator} user",
    user=administrator,
    shell="/bin/bash",
    create_home=True,
)

files.put(
    _sudo=True,
    name=f"Adding {administrator} to sudoers",
    src=StringIO(f"{administrator} ALL=(ALL:ALL) NOPASSWD:ALL"),
    dest=f"/etc/sudoers.d/{administrator}",
)

files.directory(
    _sudo=True,
    name="Creating .ssh directory",
    path=f"/home/{administrator}/.ssh",
    user=administrator,
    group=administrator,
    mode=700,
)

files.put(
    _sudo=True,
    name="Uploading local id_rsa.pub",
    src=os.path.expanduser("~") + "/.ssh/id_rsa.pub",
    dest=f"/home/{administrator}/.ssh/authorized_keys",
    user=administrator,
    group=administrator,
    mode=600,
)

files.put(
    _sudo=True,
    name="Creating bash aliases",
    src=StringIO(
        """export HISTCONTROL=ignoreboth
export HISTSIZE=100000
export HISTFILESIZE=200000

shopt -s checkwinsize
shopt -s globstar
shopt -s histappend

alias grep='grep --color=auto'
alias ls='ls --color=auto'
alias ll='ls -al'
alias lh='ll -h'
alias rm='rm -i'

alias crsnic='whois -Hh whois.crsnic.net'
alias diff='diff --color'
alias digs='dig +short'
alias dkrupg='docker-compose pull && docker image prune -f'
alias dkrupgrun='docker-compose pull && docker-compose up --force-recreate --build -d && docker image prune -f'
alias icanhazip='curl ipv4.icanhazip.com'
alias inst='dpkg --get-selections | grep -i'
alias ports='sudo lsof -i -P -n +c0 | grep LISTEN'
alias rsync='rsync --progress'
alias show='apt-cache show'
alias torget='curl --socks5-hostname localhost:9050'

domip() { curl -vsH "Host: $1" $2 | less; }
shoip() { curl -s "https://internetdb.shodan.io/$1" | jq; }
sshmnt() { mkdir -p /tmp/$1 && sshfs $1:$2 /tmp/$1; }
wayback() { curl -s "http://web.archive.org/cdx/search/cdx?url=$1&matchType=domain&collapse=urlkey&fl=timestamp,original" | sort -ru; }
whois() { /usr/bin/whois "$@" | awk '/>>>/{exit} {print}'; }
whoisc() { echo -n "$1 "; whois -h domaincheck.auda.org.au $1; }"""
    ),
    dest=f"/home/{administrator}/.bash_aliases",
    user=administrator,
    group=administrator,
    mode=600,
)

for i, dotfile in enumerate([".curlrc", ".wgetrc"]):
    files.put(
        _sudo=True,
        name=f"Creating {dotfile}",
        src=StringIO(
            "user-agent={0}{1}{0}".format(
                "" if i else '"',
                random.choice(useragents),
            ),
        ),
        dest=f"/home/{administrator}/{dotfile}",
        user=administrator,
        group=administrator,
        mode=600,
    )
