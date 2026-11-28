#!/bin/sh
set -eu
package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
exec node "$package_dir/run.mjs" "$@"
