#!/bin/sh
# Shared implementation for operator-run agent installers; launchers never call this.
install_macos_agent() (
  set -eu
  agent_dir=$1
  profile=$2
  shift 2
  agent_name=${agent_dir##*/}
  repo_dir=$(CDPATH= cd -- "$agent_dir/../.." && pwd -P)
  prefix=${HOME:?HOME must be set}/.local
  controls_dir=

  fail() { printf 'Agent install failed: %s\n' "$*" >&2; exit 1; }
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --prefix|--controls)
        [ "$#" -ge 2 ] && [ -n "$2" ] || fail "$1 requires a directory"
        if [ "$1" = --prefix ]; then prefix=$2; else controls_dir=$2; fi
        shift 2
        ;;
      -h|--help)
        printf 'Usage: %s/install.macos.sh [--prefix DIRECTORY] [--controls CHECKOUT]\n' "$agent_dir"
        printf '\nInstall %s for macOS (Apple Silicon or Intel).\n' "$agent_name"
        printf 'Requires an existing Homebrew installation. Installs Node.js, ripgrep,\n'
        printf 'Pi 1.0.3, and the Controls SDK / adapter dependencies.\n'
        if [ "$profile" = go ]; then printf 'Also installs Go, gopls (MCP), and golangci-lint.\n'; fi
        printf '\nDefault prefix: $HOME/.local; Controls: PREFIX/share/pragma/controls,\n'
        printf 'or the sibling controls checkout. --controls selects another checkout.\n'
        printf 'Does not select credentials, change factory.yaml, or start an agent.\n'
        exit 0
        ;;
      *) fail "Unknown option: $1 (use --help)" ;;
    esac
  done
  [ "$(uname -s)" = Darwin ] || fail 'This installer targets macOS.'
  case "$(uname -m)" in arm64|x86_64) architecture=$(uname -m) ;; *) fail 'Unsupported macOS architecture' ;; esac
  brew_command=$(command -v brew) || fail 'Homebrew must already be installed and on PATH.'
  command -v git >/dev/null 2>&1 || fail 'Git is required.'
  case "$profile" in core|go) ;; *) fail "Unknown dependency profile: $profile" ;; esac

  mkdir -p "$prefix"
  prefix=$(CDPATH= cd -- "$prefix" && pwd -P)
  if [ -z "$controls_dir" ]; then
    if [ -d "$prefix/share/pragma/controls" ]; then controls_dir=$prefix/share/pragma/controls
    else controls_dir=$repo_dir/../controls
    fi
  fi
  [ -d "$controls_dir/sdk/typescript" ] && [ -d "$controls_dir/adapters/pi" ] ||
    fail 'Controls SDK / Pi adapter not found. Run the system installer first or pass --controls CHECKOUT.'
  controls_dir=$(CDPATH= cd -- "$controls_dir" && pwd -P)
  bin_dir=$prefix/bin
  mkdir -p "$bin_dir"
  brew_bin=$("$brew_command" --prefix)/bin
  PATH=$bin_dir:$brew_bin:$PATH
  export PATH

  printf '\n==> Install %s dependencies (macOS/%s)\n' "$agent_name" "$architecture"
  if [ "$profile" = go ]; then "$brew_command" install node ripgrep go gopls golangci-lint
  else "$brew_command" install node ripgrep
  fi
  npm_config_engine_strict=true
  export npm_config_engine_strict
  if [ ! -x "$bin_dir/pi" ] || [ "$("$bin_dir/pi" --version 2>/dev/null || true)" != 1.0.3 ]; then
    npm install --global --prefix "$prefix" --ignore-scripts --no-audit --no-fund @earendil-works/pi-coding-agent@1.0.3
  fi
  [ "$("$bin_dir/pi" --version)" = 1.0.3 ] || fail 'Pi 1.0.3 is required by the configured runtime adapter.'

  printf '\n==> Install bundle SDK / adapter dependencies\n'
  npm ci --prefix "$controls_dir" --include=dev --no-audit --no-fund
  # Use the selected Controls installation, preserving package.json and its lock.
  # The repository defaults assume a sibling checkout; --no-save overrides only
  # the local node_modules links, so system-installer layouts work as well.
  npm install --prefix "$repo_dir" --no-save --package-lock=false --install-links=false --no-audit --no-fund \
    "$controls_dir/sdk/typescript" "$controls_dir/adapters/pi"

  printf '\n==> Verify agent prerequisites\n'
  set -- --agent "$bin_dir/pi" --profile "$agent_dir/pi" --require rg
  if [ "$profile" = go ]; then
    set -- "$@" --require go --require gofmt --require golangci-lint
    gopls help mcp >/dev/null
  fi
  node "$agent_dir/../scripts/preflight.mjs" "$@"
  (
    cd -- "$repo_dir"
    node --input-type=module -e 'import {accessSync} from "node:fs"; import {fileURLToPath} from "node:url"; for (const name of ["@pragma/controls-sdk/result-client", "@pragma/adapter-pi/session"]) accessSync(fileURLToPath(import.meta.resolve(name)));'
  )
  printf '\nInstalled %s. Keep %s and %s on the Factory service PATH.\n' "$agent_name" "$bin_dir" "$brew_bin"
)
