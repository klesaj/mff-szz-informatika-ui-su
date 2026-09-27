#!/usr/bin/env bash
# Sestaví studijní materiál daného okruhu pomocí LuaLaTeX + latexmk.
# Aux/tmp soubory -> tmp/, výsledné PDF -> out/, src/ zůstává čistý.
#
# Použití:
#   ./build.sh <cesta-k-okruhu>        # např. ./build.sh 03_specializace_ui_su/S3_strojove_uceni
#   ./build.sh <cesta> clean           # smaže tmp/ a out/
#   ./build.sh all                     # sestaví všechny okruhy, které mají src/main.tex
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export TEXINPUTS="$ROOT/common_latex:${TEXINPUTS:-}"

build_one() {
  local dir="$1"
  if [[ ! -f "$dir/src/main.tex" ]]; then
    echo "  preskakuji $dir (chybí src/main.tex)"; return 0
  fi
  echo ">> sestavuji: $dir"
  ( cd "$dir" && latexmk -lualatex -interaction=nonstopmode -file-line-error \
      -outdir=out -auxdir=tmp src/main.tex )
  echo "   hotovo: $dir/out/main.pdf"
}

clean_one() {
  local dir="$1"
  ( cd "$dir" && latexmk -outdir=out -auxdir=tmp -C src/main.tex 2>/dev/null || true )
  rm -rf "$dir/tmp"/* 2>/dev/null || true
  echo "   vyčištěno: $dir"
}

if [[ "${1:-}" == "all" ]]; then
  find "$ROOT" -type f -name main.tex -path '*/src/*' | while read -r f; do
    build_one "$(dirname "$(dirname "$f")")"
  done
  exit 0
fi

target="${1:?Použití: ./build.sh <cesta-k-okruhu> [clean] | ./build.sh all}"
if [[ "${2:-}" == "clean" ]]; then
  clean_one "$target"
else
  build_one "$target"
fi
