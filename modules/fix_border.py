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
    '-c', shlex.quote(config.border_color),
    '-x',
    '-v'
]
if config.resize:
    command.append('-r')
logger.debug(f"Fix Border command with args: {command}")


# Main function
def main():
    if config.run:
        logger.info("Running fix_border")
        call_script(command, logger)
    else:
        logger.info("Skipping fix_border.py")
