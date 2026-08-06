#!/usr/bin/env bash

set -euo pipefail

MODE="${1:-}"

case "$MODE" in
  classic|babochki)
    ;;
  *)
    echo "Использование:"
    echo "  $0 classic"
    echo "  $0 babochki"
    exit 2
    ;;
esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSETS="$ROOT/app_server/assets"

SOURCE="$ASSETS/site-config.$MODE.json"
TARGET="$ASSETS/site-config.json"
BACKUP="$ASSETS/site-config.last.json"

if [[ ! -f "$SOURCE" ]]; then
  echo "ОШИБКА: не найден файл:"
  echo "$SOURCE"
  exit 1
fi

python3 - "$SOURCE" "$MODE" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
expected_theme = sys.argv[2]

config = json.loads(path.read_text(encoding="utf-8"))
actual_theme = config.get("site", {}).get("theme")

if actual_theme != expected_theme:
    raise SystemExit(
        f"ОШИБКА: в {path.name} указана тема {actual_theme!r}, "
        f"ожидалась {expected_theme!r}"
    )

print("JSON корректный.")
print("Название:", config.get("site", {}).get("name"))
print("Тема:", actual_theme)
PY

if [[ -f "$TARGET" ]]; then
  cp -a "$TARGET" "$BACKUP"
fi

TEMP="$(mktemp "$ASSETS/.site-config.json.XXXXXX")"
cp "$SOURCE" "$TEMP"
mv "$TEMP" "$TARGET"

echo
echo "Активирован конфиг: $MODE"
echo "Резервная копия: $BACKUP"
echo
echo "Для применения выполните:"
echo "  cd $ROOT"
echo "  docker compose up assets"
