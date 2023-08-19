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
    logger.info("Step 1: Running")
    sync_gdrive.main()
    logger.info("Step 1: Finished")


async def step_two():
    logger.info("Step 2: Running")
    renamer.main()
    logger.info("Step 2: Finished")


async def step_three():
    logger.info("Step 3: Running")
    fix_border.main()
    logger.info("Step 3: Finished")


# Run tasks immediately if run_now is True
async def run_tasks(run_now):
    if run_now:
        await step_one()
        await step_two()
        await step_three()


# Create and run the asyncio event loop
async def main():
    # Read the value of the environment variable RUN_NOW, defaulting to False
    run_now = os.getenv("RUN_NOW", "False").lower() == "true"

    # Read the hour at which tasks should be scheduled from the environment, defaulting to 5 if not set
    scheduled_hour = int(os.getenv("SCHEDULED_HOUR", "5"))

    # Run tasks immediately (if run_now is True)
    await run_tasks(run_now)

    while True:
        # Get the current time
        now = datetime.now()

        # Calculate the next run time based on the specified hour
        next_run = datetime(now.year, now.month, now.day, scheduled_hour, 0)

        # If the next run time has already passed for today, set it for the same time tomorrow
        if now >= next_run:
            next_run += timedelta(days=1)

        # Calculate the number of seconds to wait until the next run
        wait_seconds = (next_run - now).total_seconds()
        logger.info(f"Sleep duration: {wait_seconds}")

        await asyncio.sleep(wait_seconds)

        # Run scheduled tasks
        await run_tasks(True)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
