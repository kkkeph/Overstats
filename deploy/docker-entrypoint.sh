#!/bin/bash
set -e

# This entrypoint runs as root (declared before USER in Dockerfile) so we can
# fix permissions on Docker volumes that may be root-owned on first run.

# Ensure runtime cache directories exist and are writable.
for dir in /opt/overstats/cache /opt/overstats/src/db; do
    if [ -d "$dir" ]; then
        chown -R overstats:overstats "$dir" 2>/dev/null || true
    fi
done

mkdir -p /opt/overstats/cache/patch_notes/images 2>/dev/null || true
chown -R overstats:overstats /opt/overstats/cache /opt/overstats/src/db 2>/dev/null || true

# Drop privileges to the 'overstats' user and exec the CMD.
# Prefer runuser, fall back to su (both are in util-linux / shadow).
if command -v runuser >/dev/null 2>&1; then
    exec runuser -u overstats -- "$@"
else
    exec su -s /bin/sh -c 'exec "$0" "$@"' overstats -- "$@"
fi
