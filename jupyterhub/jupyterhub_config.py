"""
JupyterHub config for the littlest jupyterhub.
"""

from pathlib import Path
from secrets import token_hex
import stat

from traitlets.log import get_logger

log = get_logger()

c = get_config()  # noqa

install_path = Path("/opt/jupyterhub")
jupyterhub_dir = install_path / "jupyterhub"
secrets_dir = install_path / "secrets"
if not secrets_dir.exists():
    secrets_dir.mkdir(mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP, exist_ok=True)

mode = secrets_dir.stat().st_mode
if mode & stat.S_IRWXO:
    log.warning(f"secrets dir {secrets_dir} has world-access. Locking it down.")
    secrets_dir.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)


traefik_password_file = secrets_dir / "traefik-password"
cookie_secret_file = secrets_dir / "cookie-secret"
db_file = secrets_dir / "jupyterhub.sqlite"
db_file = db_file

c.TraefikProxy.traefik_api_username = "jupyterhub"

for secret_file in (traefik_password_file, cookie_secret_file):
    if not secret_file.exists():
        log.info(f"Generating secret in {secret_file}")
        with secret_file.open("w") as f:
            f.write(token_hex(32))

with cookie_secret_file.open() as f:
    c.JupyterHub.cookie_secret = f.read().strip()

with traefik_password_file.open() as f:
    c.TraefikProxy.traefik_api_password = f.read().strip()

c.JupyterHub.db_url = f"sqlite:///{db_file}"

# leave users running when the Hub restarts
c.JupyterHub.cleanup_servers = False

# externally managed traefik
c.TraefikProxy.traefik_entrypoint = "https"
c.TraefikProxy.should_start = False
c.JupyterHub.proxy_class = "traefik_file"

# where jupyterhub rules go
c.TraefikFileProviderProxy.dynamic_config_file = str(
    install_path / "traefik/dynamic/jupyterhub.toml"
)

# public URL of this Hub
c.JupyterHub.public_url = "https://longs.stat.berkeley.edu"

# Authenticator setup
c.JupyterHub.authenticator_class = "local-github"
c.GitHubOAuthenticator.client_id = "Ov23liHQyt7EfrqR89xm"
with (secrets_dir / "client_secret").open() as f:
    c.GitHubOAuthenticator.client_secret = f.read()

# only allow usernames from config
c.Authenticator.allow_existing_users = False

# map github username to local system username, if different
c.Authenticator.username_map = username_map = {}

c.GitHubOAuthenticator.allowed_users = {
    "fperez",
    "fperezhub",
    "minrk",
    "ryanlovett",
    "paciorek",
    "mfisher87",
    "tsnow03",
    "cassiebuhler",
    "cboettig",
}

c.Spawner.cmd = ["/opt/jupyterhub/jupyterhub/start-singleuser.sh"]

c.Spawner.environment = {
    "HF_HOME": "/opt/huggingface",
    "OLLAMA_MODELS": "/opt/ollama",
    "OPENCODE_CONFIG_DIR": "/opt/jupyterhub/opencode",
    "OPENCODE_CONFIG": "/opt/jupyterhub/opencode/opencode.json",
}
c.JupyterHub.log_level = 10

# shared access to the `fperezhub` user

c.JupyterHub.load_roles = [
    {
        # populate admin role rather than admin_users
        # that way, we can revoke permission in config,
        # rather than only granting
        "name": "admin",
        "users": [
            "fperez",
            "ryanlovett",
            "minrk",
            "paciorek",
        ],
    },
    {
        "name": "fperezhub",
        "scopes": [
            "admin-ui",
            "list:users!user=fperezhub",
            "read:users!user=fperezhub",
            "servers!user=fperezhub",
            "access:servers!user=fperezhub",
        ],
        "users": [
            "minrk",
            "fperez",
            "mfisher87",
            "tsnow03",
            "cassiebuhler",
            "cboettig",
        ],
    },
]

# default to /hub/home because some users can't start their own servers
c.JupyterHub.default_url = "/hub/home"
