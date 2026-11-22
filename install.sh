#!/bin/sh
# Install the Factory control plane and Monitor. Project workflows are configured separately.
set -eu

usage() {
  cat <<'EOF'
Usage: ./install.sh [--prefix DIRECTORY]

Install Controls and Monitor from main. Re-running fast-forwards clean main
checkouts and rebuilds them. Existing services are not started or restarted.

  --prefix DIRECTORY  Installation prefix (default: $HOME/.local)
  -h, --help          Show this help

Requires Git, Go, Node.js and npm. Dependency versions follow the repositories.
Installs binaries in PREFIX/bin and keeps sources in PREFIX/share/pragma.
Worker packages, agent runtimes, credentials and factory.yaml are project choices.
EOF
}
fail() { printf 'Install failed: %s\n' "$*" >&2; exit 1; }
progress() { printf '\n==> %s\n' "$*"; }

prefix=${HOME:?HOME must be set}/.local
while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail '--prefix requires a directory'
      prefix=$2
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown option: $1 (use --help)" ;;
  esac
done

missing=
for tool in git go node npm; do
  if ! command -v "$tool" >/dev/null 2>&1; then missing="$missing $tool"; fi
done
[ -z "$missing" ] || fail "Missing prerequisites:$missing"
case "$(uname -s)" in Darwin|Linux) ;; *) fail 'This installer supports macOS and Linux.' ;; esac

mkdir -p "$prefix"
prefix=$(CDPATH= cd -- "$prefix" && pwd -P)
bin_dir=$prefix/bin
sources=$prefix/share/pragma
mkdir -p "$bin_dir" "$sources"
PATH=$bin_dir:$PATH
export PATH
# npm checks the actual package engines on main; include build dependencies even
# when the invoking shell sets NODE_ENV=production.
npm_config_engine_strict=true
export npm_config_engine_strict

checkout() {
  repository=$1
  destination=$2
  if [ ! -e "$destination" ]; then
    git clone --branch main --single-branch "$repository" "$destination"
    return
  fi
  [ -d "$destination" ] || fail "Not a directory: $destination"
  installed_root=$(git -C "$destination" rev-parse --show-toplevel 2>/dev/null) || fail "Not a Git checkout: $destination"
  actual_root=$(CDPATH= cd -- "$destination" && pwd -P)
  [ "$installed_root" = "$actual_root" ] || fail "Not a dedicated checkout: $destination"
  origin=$(git -C "$destination" config --get remote.origin.url)
  [ "$origin" = "$repository" ] || fail "Unexpected origin in $destination"
  branch=$(git -C "$destination" symbolic-ref --quiet --short HEAD) || fail "Detached checkout: $destination"
  [ "$branch" = main ] || fail "Expected main in $destination; found $branch"
  [ -z "$(git -C "$destination" status --porcelain)" ] || fail "Local changes in $destination; resolve them before updating"
  git -C "$destination" pull --ff-only origin main
}

controls=$sources/controls
monitor=$sources/monitor
progress 'Get Controls and Monitor from main'
checkout https://github.com/PragmaEngineering/factory-controller.git "$controls"
checkout https://github.com/PragmaEngineering/factory-monitor.git "$monitor"

progress 'Install Controls and its SDK / adapter dependencies'
npm ci --prefix "$controls" --include=dev --no-audit --no-fund
"$controls/install.sh" "$bin_dir"

progress 'Build and install Monitor'
(
  cd -- "$monitor"
  npm ci --include=dev --no-audit --no-fund
  npm run build
  npm_config_prefix="$prefix" npm link --no-audit --no-fund
)

progress 'Verify installed commands'
"$bin_dir/factory" --help >/dev/null
"$bin_dir/pragma-monitor" --help >/dev/null
printf '\nInstalled: %s/factory\n           %s/pragma-monitor\n' "$bin_dir" "$bin_dir"
printf 'Keep %s on PATH and retain %s.\n' "$bin_dir" "$sources"
printf '\nDefine factory.yaml in your project and provision its selected worker packages.\n'
printf 'Then run: factory start\n          factory monitor start -d\n'
printf 'Submit:   factory exec "Your task" -c /path/to/project/factory.yaml\n'
