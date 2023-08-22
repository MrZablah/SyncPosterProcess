import subprocess


def call_script(command, logger):
    try:
        # Run the Bash script with arguments and capture stdout and stderr
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Capture output as text (Python 3.5 and later)
        )

        # Read and print stdout and stderr line by line
        for line in process.stdout:
            logger.info(line.strip())

        for line in process.stderr:
            logger.info(line.strip())

        # Wait for the process to finish
        process.wait()

        # Check the exit code to handle errors if needed
        if process.returncode != 0:
            logger.debug(f"Bash script returned a non-zero exit code: {process.returncode}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running the Bash script: {e}")
