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
debug_cmd = command.copy()
debug_cmd[debug_cmd.index('-i') + 1] = '<redacted>' if config.client_id else 'None'
debug_cmd[debug_cmd.index('-s') + 1] = '<redacted>' if config.client_secret else 'None'
debug_cmd[debug_cmd.index('-t') + 1] = '<redacted>' if config.token else 'None'
logger.debug(f"RClone command with args: {debug_cmd}")


# Main function
def main():
    if config.run:
        logger.info("Running sync_gdrive")
        call_script(command, logger)
        logger.info("Finished sync_gdrive")
    else:
        logger.info("Skipping sync_gdrive.py")
