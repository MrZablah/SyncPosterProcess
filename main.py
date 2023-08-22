import os
import schedule
import asyncio
from modules import sync_gdrive, renamer, fix_border
from utility.logger import setup_logger
from utility.config import Config
from datetime import datetime, timedelta

config = Config(script_name="global")
logger = setup_logger(config.log_level, "global")


async def step_one():
    logger.debug("Step 1: Running")
    sync_gdrive.main()
    logger.debug("Step 1: Finished")


async def step_two():
    logger.debug("Step 2: Running")
    renamer.main()
    logger.debug("Step 2: Finished")


async def step_three():
    logger.debug("Step 3: Running")
    fix_border.main()
    logger.debug("Step 3: Finished")


# Run tasks immediately if run_now is True
async def run_tasks(run_now):
    if run_now:
        await step_one()
        await step_two()
        await step_three()


# Create and run the asyncio event loop
async def main():
    # Run tasks immediately (if run_now is True)
    await run_tasks(config.run_now)

    while True:
        # Get the current time
        now = datetime.now()

        # Calculate the next run time based on the specified hour
        next_run = datetime(now.year, now.month, now.day, int(config.schedule_hour), 0)

        # If the next run time has already passed for today, set it for the same time tomorrow
        if now >= next_run:
            next_run += timedelta(days=1)

        # Calculate the number of seconds to wait until the next run
        wait_seconds = (next_run - now).total_seconds()
        logger.info(f"Sleep duration in seconds: {wait_seconds}")

        await asyncio.sleep(wait_seconds)

        # Run scheduled tasks
        await run_tasks(True)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
