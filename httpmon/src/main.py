import argparse
import asyncio
import logging
import sys

from services import HealthCheckerService, YamlReaderService

logger = logging.getLogger(__name__)


async def main(args):
    targets_list = YamlReaderService.read_yaml(args.config)

    async with HealthCheckerService.create_session() as session:
        health_results = await asyncio.gather(
            *[
                HealthCheckerService.check_health_async(session, target)
                for target in targets_list
            ],
            return_exceptions=False,
        )
        print(health_results)

    if all(result.is_healthy for result in health_results):
        logger.info(f"Target Urls Report: {health_results}")
        sys.exit(0)
    else:
        logger.info(f"Target Urls Report: {health_results}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", metavar="str", type=str)
    args = parser.parse_args()
    asyncio.run(main(args))
