import shlex
from utility.logger import setup_logger, get_logger_file
from utility.config import Config
from utility.call_script import call_script

config = Config(script_name="fix_border")
logger = setup_logger(config.log_level, "fix_border")
log_file = get_logger_file("fix_border")

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
logger.debug(f"Fix Border command with args: {command}")


# Main function
def main():
    call_script(command, logger)
