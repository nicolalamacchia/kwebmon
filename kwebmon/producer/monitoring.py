import asyncio
import re
from datetime import datetime
from typing import Callable, Any

import aiohttp

REQUEST_TIMEOUT = 5


class Monitor:
    """
    Websites monitor: periodically checks the health of input websites.
    """

    def __init__(
        self,
        target_websites: list[dict],
        response_callback: Callable[[dict, dict], Any]
    ) -> None:
        self._sites = self._compile_patterns(target_websites)
        self._response_times = {}
        self._response_callback = response_callback

    @staticmethod
    def _compile_patterns(target_websites: list[dict]) -> list[dict]:
        compiled_re_sites = []
        for site in target_websites:
            try:
                compiled_pattern = re.compile(site["pattern"])
            except KeyError:
                compiled_re_sites.append(site)
            else:
                compiled_re_sites.append({
                    "url": site["url"],
                    "pattern": compiled_pattern
                })
        return compiled_re_sites

    @staticmethod
    async def _on_request_start(session, context, params):
        context.start = asyncio.get_event_loop().time()

    async def _on_request_end(self, session, context, params):
        url = str(params.url)
        total_time = asyncio.get_event_loop().time() - context.start
        self._response_times[url] = total_time

    async def _get(self, client_session, site):
        url = site["url"]
        pattern = site.get("pattern")
        now = datetime.utcnow().isoformat()
        stats = {}
        request_data = {
            "url": url,
            "pattern": pattern.pattern if pattern else None
        }

        try:
            response = await client_session.request("GET", url)
        except aiohttp.client_exceptions.ClientConnectorError:
            stats["utc_completed_at"] = now
            stats["error"] = "Invalid domain"
            self._response_callback(request_data, stats)
            return

        text = await response.text(encoding="utf-8")

        stats["status_code"] = response.status
        stats["utc_completed_at"] = now
        stats["response_time"] = self._response_times.pop(url)

        if response.ok and pattern:
            stats["is_content_valid"] = bool(pattern.search(text))

        self._response_callback(request_data, stats)

    async def check(self) -> None:
        """
        Checks if the specified websites are healthy and collects
        metrics.

        :returns: metrics collected for each website
        """

        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(self._on_request_start)
        trace_config.on_request_end.append(self._on_request_end)

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT),
            trace_configs=[trace_config]
        ) as client_session:
            tasks = [self._get(client_session, site) for site in self._sites]
            await asyncio.gather(*tasks)

    async def loop(self, check_interval: int) -> None:
        """
        Monitors continuously the input websites in an infinite loop and
        yields health metrics for each check.

        :param check_interval: interval in seconds between checks
        :returns: metrics collected for each website
        """

        while True:
            await self.check()
            await asyncio.sleep(check_interval)
