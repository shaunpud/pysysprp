import re

from io import StringIO
from pyinfra.operations import files, server

hostname = input("\nHostname: ")
if not hostname or not re.match(r"^[a-z0-9-\.]+$", hostname, flags=re.I):
    exit("Invalid hostname")

files.directory(
    _sudo=True,
    name="Creating working directory",
    path="/opt/adminer/public/",
)

files.download(
    _sudo=True,
    name="Downloading adminer",
    src="https://www.adminer.org/latest-en.php",
    dest="/opt/adminer/public/index.php",
)

files.download(
    _sudo=True,
    name="Downloading dracula skin",
    src="https://raw.githubusercontent.com/vrana/adminer/master/designs/dracula/adminer.css",
    dest="/opt/adminer/public/adminer.css",
)

files.put(
    _sudo=True,
    name="Creating nginx config",
    src=StringIO(
        f"""server {{
    listen 80;

    server_name {hostname};

    root /opt/adminer/public/;

    index index.php;

    access_log /var/log/nginx/adminer-access.log combined;
    error_log /var/log/nginx/adminer-error.log;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass 127.0.0.1:9000;
    }}
}}"""
    ),
    dest="/opt/adminer/nginx.conf",
)

files.link(
    _sudo=True,
    name="Creating symlink",
    path=f"/etc/nginx/sites-enabled/{hostname}",
    target="/opt/adminer/nginx.conf",
)

server.service(
    _sudo=True,
    name="Reloading nginx",
    service="nginx",
    reloaded=True,
)
