#!/bin/bash

PUID=${PUID:-100}
PGID=${PGID:-99}
UMASK=${UMASK:-002}

umask $UMASK
groupmod -o -g "$PGID" dockeruser
usermod -o -u "$PUID" dockeruser

chown -R dockeruser:dockeruser /app /config

exec runuser -u dockeruser -g dockeruser -- "$@"