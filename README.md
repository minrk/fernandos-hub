# Deployment resources for Fernando's JupyterHub

Deployed on a Mac in his office.

## TODO

- start login shells
- process for adding users
- setup local model server?

## Deployment notes

- this repo cloned at: /opt/jupyterhub
- envs with pixi:
  - hub environment: /opt/conda/.pixi/envs/hub
  - user environment: /opt/conda/.pixi/envs/user
- jupyterhub is root (needs to be for PAM)
- traefik is root (shouldn't be, see below)
- user environment must be world-readable
- some directories (mainly `secrets` must not be world-readable)
- update envs with `pixi install -a`

launchdaemon docs: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html

Making a system user for traefik:

[ref](https://serverfault.com/questions/182347/add-daemon-account-on-os-x)

```
username_=traefik
uid_=405
realname_="Traefik Daemon"

dscl . -create /Groups/_$username_
dscl . -create /Groups/_$username_ PrimaryGroupID $uid_
dscl . -create /Groups/_$username_ RecordName _$username_ $username_
dscl . -create /Groups/_$username_ RealName $realname_
dscl . -create /Groups/_$username_ Password \*

dscl . -create /Users/_$username_
dscl . -create /Users/_$username_ NFSHomeDirectory /xpt/local/apache2/wsgi/api
dscl . -create /Users/_$username_ Password \*
dscl . -create /Users/_$username_ PrimaryGroupID $uid_
dscl . -create /Users/_$username_ RealName $realname_
dscl . -create /Users/_$username_ RecordName _$username_ $username_
dscl . -create /Users/_$username_ UniqueID $uid_
dscl . -create /Users/_$username_ UserShell /usr/bin/false
dscl . -delete /Users/_$username_ PasswordPolicyOptions
dscl . -delete /Users/_$username_ AuthenticationAuthority
```

Not currently using that, though, because traefik user needs access to the `dynamic/jupyterhub.toml` file,
so both are root for now.
Need to figure out how to make that appropriately readable by the traefik user
when the Hub writes it as root.

## Tasks

generally assumes we always start with:

```
cd /opt/jupyterhub
git pull
pixi install -a
```

### Update envs

Add a package to the user env with e.g. `pixi add -f user packagename`

Update the installs:

```
pixi install -a
```

### reload jupyterhub and/or traefik config:

```
pixi run reload-daemons
```

### Check logs

Mainly:

- /Library/Log/jupyterhub/jupyterhub.log
- /Library/Log/jupyterhub/traefik/traefik.log
