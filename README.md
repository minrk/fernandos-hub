# Deployment resources for Fernando's JupyterHub

Deployed on a Mac in his office.

## Deployment notes

- this repo: /opt/jupyterhub
- envs with pixi:
  - hub environment: /opt/conda/.pixi/envs/hub
  - user environment: /opt/conda/.pixi/envs/user

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
