import re

from io import StringIO
from pyinfra.operations import files, git, server

hostname = input("\nHostname: ")
if not hostname or not re.match(r"^[a-z0-9-\.]+$", hostname, flags=re.I):
    exit("Invalid hostname")

git.repo(
    _sudo=True,
    name="Cloning repository",
    src="https://github.com/ptrofimov/beanstalk_console.git",
    dest="/opt/beanstalk_console",
)

files.file(
    _sudo=True,
    name="Update permissions",
    path="/opt/beanstalk_console/storage.json",
    user="www-data",
    group="www-data",
    mode=660,
)

files.put(
    _sudo=True,
    name="Creating nginx config",
    src=StringIO(
        f"""server {{
    listen 80;

    server_name {hostname};

    root /opt/beanstalk_console/public/;

    index index.php;

    access_log /var/log/nginx/beanstalk_console-access.log combined;
    error_log /var/log/nginx/beanstalk_console-error.log;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass 127.0.0.1:9000;
    }}
}}"""
    ),
    dest="/opt/beanstalk_console/nginx.conf",
)

files.link(
    _sudo=True,
    name="Creating symlink",
    path="/etc/nginx/sites-enabled/beanstalk_console.conf",
    target="/opt/beanstalk_console/nginx.conf",
)

server.service(
    _sudo=True,
    name="Reloading nginx",
    service="nginx",
    reloaded=True,
)
