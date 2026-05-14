#!/usr/bin/env bash
# Runs on GitHub Actions after checkout. Env:
#   COMPONENT, DEPLOY_BRANCH, STANDS_CSV, DEPLOY_SSH_KEY,
#   DEPLOY_PROJECT_PATH — в CI из Variables; SERVER_SSH_USER — из Variables (дефолтный SSH login)
#
# Stand map JSON (same shape as .github/workflows/stands.example.json), from in order:
#   1) DEPLOY_STANDS_JSON_SECRET — repo Secret DEPLOY_STANDS_JSON (optional)
#   2) DEPLOY_STANDS_JSON_VAR    — repo Variable DEPLOY_STANDS_JSON
#   3) File DEPLOY_STANDS_MAP or deploy/stands.json (optional, local / fallback)
#
# stands_csv: comma-separated aliases matching JSON object keys (case-insensitive).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REMOTE_SCRIPT="$SCRIPT_DIR/deploy-remote.sh"
LOCAL_MAP_FALLBACK="${DEPLOY_STANDS_MAP:-$ROOT_DIR/deploy/stands.json}"

COMPONENT="${COMPONENT:?}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:?}"
STANDS_CSV="${STANDS_CSV:?}"
SERVER_SSH_USER="${SERVER_SSH_USER-}"
DEPLOY_SSH_KEY="${DEPLOY_SSH_KEY:?}"
DEPLOY_PROJECT_PATH="${DEPLOY_PROJECT_PATH-}"

command -v jq >/dev/null || {
  echo "jq is required (install on runner)" >&2
  exit 1
}

resolve_stands_json() {
  local s="${DEPLOY_STANDS_JSON_SECRET-}"
  local v="${DEPLOY_STANDS_JSON_VAR-}"
  if [[ -n "${s}" ]]; then
    printf '%s' "$s"
    return 0
  fi
  if [[ -n "${v}" ]]; then
    printf '%s' "$v"
    return 0
  fi
  if [[ -f "$LOCAL_MAP_FALLBACK" ]]; then
    cat "$LOCAL_MAP_FALLBACK"
    return 0
  fi
  echo "Configure stand map: set repository Variable DEPLOY_STANDS_JSON (JSON), or Secret DEPLOY_STANDS_JSON to override." >&2
  echo "Optional local file: $LOCAL_MAP_FALLBACK" >&2
  return 1
}

MAP_FILE="$(mktemp)"
KEY_FILE="$(mktemp)"
cleanup() {
  rm -f "$MAP_FILE" "$KEY_FILE"
}
trap cleanup EXIT

if ! resolve_stands_json >"$MAP_FILE"; then
  exit 1
fi

if ! jq -e 'type == "object"' "$MAP_FILE" >/dev/null 2>&1; then
  echo "DEPLOY_STANDS_JSON must be a JSON object with stand aliases as keys." >&2
  exit 1
fi

list_allowed_aliases() {
  jq -r 'keys[]' "$MAP_FILE" | sort -u
}

canonical_alias() {
  local raw="$1"
  raw="$(echo "$raw" | tr -d '[:space:]')"
  raw="$(echo "$raw" | tr '[:upper:]' '[:lower:]')"
  local k
  while IFS= read -r k; do
    [[ "$(echo "$k" | tr '[:upper:]' '[:lower:]')" == "$raw" ]] && echo "$k" && return 0
  done < <(jq -r 'keys[]' "$MAP_FILE")
  echo "Unknown stand alias '$1'. Allowed: $(list_allowed_aliases | paste -sd, -)" >&2
  return 1
}

host_for_alias() {
  local key="$1"
  local h
  h="$(jq -r --arg k "$key" '.[$k].host // empty' "$MAP_FILE")"
  if [[ -z "$h" || "$h" == "null" ]]; then
    echo "Stand '$key' has no host in stands map" >&2
    return 1
  fi
  echo "$h"
}

path_for_alias() {
  local key="$1"
  local p
  p="$(jq -r --arg k "$key" '.[$k].path // empty' "$MAP_FILE")"
  if [[ -n "$p" && "$p" != "null" ]]; then
    echo "$p"
    return 0
  fi
  if [[ -n "${DEPLOY_PROJECT_PATH}" ]]; then
    echo "$DEPLOY_PROJECT_PATH"
    return 0
  fi
  echo "Stand '$key' has no \"path\" and DEPLOY_PROJECT_PATH variable is unset." >&2
  return 1
}

user_for_alias() {
  local key="$1"
  local u
  u="$(jq -r --arg k "$key" '.[$k].user // empty' "$MAP_FILE")"
  if [[ -n "$u" && "$u" != "null" ]]; then
    echo "$u"
    return 0
  fi
  if [[ -n "${SERVER_SSH_USER}" ]]; then
    echo "$SERVER_SSH_USER"
    return 0
  fi
  echo "Stand '$key' has no \"user\" field and SERVER_SSH_USER variable is unset — set one of them." >&2
  return 1
}

umask 077
printf '%s\n' "$DEPLOY_SSH_KEY" >"$KEY_FILE"

IFS=',' read -ra RAW_STANDS <<<"$STANDS_CSV"
if [[ ${#RAW_STANDS[@]} -eq 0 ]]; then
  echo "stands_csv is empty" >&2
  exit 1
fi

for raw in "${RAW_STANDS[@]}"; do
  [[ -z "${raw// /}" ]] && continue
  stand="$(canonical_alias "$raw")"
  host="$(host_for_alias "$stand")"
  deploy_path="$(path_for_alias "$stand")"
  ssh_user="$(user_for_alias "$stand")"
  echo ">>> [$stand] ${ssh_user}@${host} -> $deploy_path ($COMPONENT @ $DEPLOY_BRANCH)"
  ssh \
    -i "$KEY_FILE" \
    -o StrictHostKeyChecking=accept-new \
    "${ssh_user}@${host}" \
    bash -s "$COMPONENT" "$DEPLOY_BRANCH" "$deploy_path" <"$REMOTE_SCRIPT"
done
