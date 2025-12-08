import asyncio
import logging
from dataclasses import dataclass
from functools import partial
from subprocess import run
from typing import Callable

import httpx

log = logging.getLogger("healthcheck")


@dataclass(kw_only=True)
class HealthCheck:
    name: str
    failure_limit: int = 3
    start_delay: float = 0
    interval: float = 10
    on_failure: Callable | None = None

    def check(self) -> bool:
        raise NotImplementedError()

    async def run(self):
        log.info(f"Checking {self.name} every {self.interval}s")
        await asyncio.sleep(self.start_delay)
        failure_count = 0
        while True:
            try:
                result = await self.check()
            except Exception as e:
                failure_count += 1
                log.error(
                    f"Error checking {self.name}: {e}, {failure_count} / {self.failure_limit}"
                )
            else:
                if result:
                    failure_count = 0
                    log.debug(f"{self.name} check ok")
                else:
                    failure_count += 1
                    log.error(
                        f"{self.name} failed check, {failure_count} / {self.failure_limit}"
                    )

            if failure_count >= self.failure_limit:
                try:
                    await self.on_failure()
                except Exception:
                    log.exception(f"{self.name} failed on_failure hook")
            await asyncio.sleep(self.interval)


@dataclass(kw_only=True)
class HTTPCheck(HealthCheck):
    url: str
    method: str = "GET"
    timeout: int = 30

    async def check(self):
        log.info(f"{self.name} checking {self.method} {self.url}")
        async with httpx.AsyncClient(follow_redirects=False) as client:
            r = await client.request(
                method=self.method,
                url=self.url,
                timeout=self.timeout,
            )
            log.debug(f"{r.status_code} {self.method} {self.url}")
            return 200 <= r.status_code < 400


def kickstart(daemon_name: str):
    """Restart a launchdaemon with kickstart"""
    log.warning(f"Restarting {daemon_name}")
    run(["launchctl", "kickstart", "-k", f"system/{daemon_name}"], check=True)


async def main():
    logging.basicConfig(
        format="[%(name)s %(asctime)s %(levelname)s] %(message)s", level=logging.INFO
    )
    checkers = [
        HTTPCheck(
            name="traefik",
            url="http://127.0.0.1/hub/api/",
            on_failure=partial(kickstart, "org.jupyter.hub.traefik"),
        ),
        HTTPCheck(
            name="jupyterhub",
            url="http://127.0.0.1:8081/hub/api/",
            on_failure=partial(kickstart, "org.jupyter.hub.jupyterhub"),
        ),
    ]
    tasks = [asyncio.create_task(checker.run()) for checker in checkers]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
