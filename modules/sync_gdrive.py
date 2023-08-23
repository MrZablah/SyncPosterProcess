import shlex
import json
from utility.logger import setup_logger
from utility.config import Config
from utility.call_script import call_script

config = Config(script_name="sync_gdrive")
logger = setup_logger(config.log_level, "spp")

# Specify the Bash script file to run
bash_script_file = './modules/scripts/rclone.sh'
command = [
    bash_script_file,
    '-i', shlex.quote(config.client_id),
    '-s', shlex.quote(config.client_secret),
    '-l', shlex.quote(config.sync_location),
    '-f', shlex.quote(config.gdrive_id),
    '-t', json.dumps(config.token)
]
logger.debug(f"RClone command with args: {command}")


# Main function
def main():
    if config.run:
        logger.info("Running sync_gdrive")
        call_script(command, logger)
    else:
        logger.info("Skipping sync_gdrive.py")
