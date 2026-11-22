#!/bin/sh
set -eu
agent_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
. "$agent_dir/../scripts/install-common.sh"
install_macos_agent "$agent_dir" core "$@"
