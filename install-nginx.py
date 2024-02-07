from pyinfra.operations import apt, files, systemd

apt.packages(
    _sudo=True,
    name="Installing nginx",
    packages=[
        "apache2-utils",
        "nginx",
    ],
    latest=True,
    update=True,
)

files.replace(
    _sudo=True,
    name="Hide server tokens",
    path="/etc/nginx/nginx.conf",
    text="# server_tokens off;",
    replace="server_tokens off;",
)

systemd.service(
    _sudo=True,
    name="Reload nginx",
    service="nginx",
    reloaded=True,
)
