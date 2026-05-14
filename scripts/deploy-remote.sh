#!/usr/bin/env bash
# Runs on the deployment server via SSH (stdin pipe). Args: component front|back|bot, branch, deploy_path
set -euo pipefail

COMPONENT="${1:?component}"
BRANCH="${2:?branch}"
DEPLOY_PATH="${3:?deploy_path}"

cd "$DEPLOY_PATH"

git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

docker_prune() {
  docker builder prune --force || true
  mapfile -t dangling < <(docker images --filter "dangling=true" -q --no-trunc 2>/dev/null || true)
  if ((${#dangling[@]})); then
    docker rmi "${dangling[@]}" || true
  fi
}

case "$COMPONENT" in
  front)
    docker rm -f outline-assets 2>/dev/null || true
    docker compose up assets
    docker_prune
    ;;
  back)
    docker build -t outline-app-python-3.10:latest .
    docker compose up -d server
    docker_prune
    ;;
  bot)
    docker build -t outline-app-python-3.10:latest .
    docker compose up -d bot
    docker_prune
    ;;
  *)
    echo "Unknown component: $COMPONENT (expected front|back|bot)" >&2
    exit 1
    ;;
esac
