Custom scripts for [pyinfra](https://github.com/Fizzadar/pyinfra)

```bash
pipx install pyinfra==2.9.2
```

```bash
pyinfra --user root --port 2222 --password hunter2 12.34.56.78 script.py
```

```bash
pyinfra host01 exec --sudo -- apt-get install blah
```
