import shlex
from utility.logger import setup_logger
from utility.config import Config
from utility.call_script import call_script

config = Config(script_name="fix_border")
logger = setup_logger(config.log_level, "spp")

# Specify the Bash script file to run
bash_script_file = './modules/scripts/change_border.sh'
command = [
    bash_script_file,
    '-i', shlex.quote(config.input_folder),
    '-o', shlex.quote(config.output_folder),
    '-c', shlex.quote(config.border_color)
]

if config.overwrite_existing:
    command.append('-x')

if config.bottom_only:
    command.append('-b')

if config.resize:
    command.append('-r')

if config.log_level == 'debug':
    command.append('-v')
logger.debug(f"Fix Border command with args: {command}")


# Main function
def main():
    if config.run:
        logger.info("Running fix_border")
        call_script(command, logger)
        logger.info("Finished fix_border")
    else:
        logger.info("Skipping fix_border.py")
