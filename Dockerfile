# Create pipenv image to convert Pipfile to requirements.txt
FROM python:3.11-slim as pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install pipenv and convert to requirements.txt
RUN pip3 install --no-cache-dir --upgrade pipenv; \
    pipenv requirements > requirements.txt

# debug requirements.txt
RUN cat requirements.txt

FROM python:3.11-slim as python-reqs

# Copy requirements.txt from pipenv stage
COPY --from=pipenv /requirements.txt requirements.txt

# Install gcc for building python dependencies; install app dependencies
RUN apt-get update; \
    apt-get install -y gcc; \
    pip3 install --no-cache-dir -r requirements.txt

# Set base image
FROM python:3.11-slim
LABEL maintainer="MrZablah" \
      description="Sync Poster Process"

# Set working directory, copy source into container
WORKDIR /app
COPY . /app

# give permissions to all files under /modules/scripts
RUN chmod -R 777 /app/modules/scripts

# Copy python packages from python-reqs
COPY --from=python-reqs /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Script environment variables
ENV SPP_CONFIG=/config/config.yml
ENV SCHEDULE_HOUR=5
ENV RUN_NOW=true
ENV TZ=America/Monterrey
ENV SPP_CONFIG=/config/config.yml
ENV XDG_CONFIG_HOME=/config

# Delete setup files
# Create user and group to run the container
# Install imagemagick
# Clean up apt cache
# Override default ImageMagick policy XML file
RUN set -eux; \
    rm -f Pipfile Pipfile.lock; \
    groupadd -g 99 dockeruser; \
    useradd -u 100 -g 99 dockeruser; \
    apt-get update; \
    apt-get install -y --no-install-recommends wget curl unzip imagemagick libmagickcore-6.q16-6-extra tzdata; \
    cp modules/policy.xml /etc/ImageMagick-6/policy.xml

# Install rclone dependencies and rclone
RUN curl https://rclone.org/install.sh | bash && \
    apt-get remove -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# test rclone
RUN rclone --version

# logs directory
RUN mkdir -p /logs

# Entrypoint
CMD ["python", "main.py"]
ENTRYPOINT ["bash", "./start.sh"]