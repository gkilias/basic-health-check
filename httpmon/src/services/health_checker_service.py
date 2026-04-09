import time
from contextlib import asynccontextmanager

import aiohttp

from models import CheckResult, TargetConfig


class HealthCheckerService:

    @staticmethod
    @asynccontextmanager
    async def create_session():
        session = None
        try:
            session = aiohttp.ClientSession()
            yield session
        finally:
            if session:
                await session.close()

    @staticmethod
    async def check_health_async(
        session: aiohttp.ClientSession, target: TargetConfig
    ) -> CheckResult:

        try:
            start = time.perf_counter()
            async with session.get(
                target.url, timeout=aiohttp.ClientTimeout(target.timeout)
            ) as response:
                stop = time.perf_counter()
                time_taken = stop - start

            return CheckResult(
                response_time=time_taken * 1000,
                actual_status_code=response.status,
                expected_status=target.expected_status,
                error=None,
            )

        except TimeoutError as e:

            return CheckResult(
                response_time=None,
                actual_status_code=None,
                expected_status=target.expected_status,
                error=repr(e),
            )

        except aiohttp.ClientError as e:
            return CheckResult(
                response_time=None,
                actual_status_code=None,
                expected_status=target.expected_status,
                error=repr(e),
            )
