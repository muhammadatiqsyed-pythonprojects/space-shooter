#!/bin/bash
# Build the web version from a clean copy, so .venv is never packaged
set -e
STAGE=../web-build/space-shooter
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp main.py settings.py player.py bullet.py enemy.py button.py ui.py "$STAGE"/
cp -r assets "$STAGE"/
(cd "$STAGE" && pygbag --build .)
rm -rf docs
mkdir -p docs
cp -r "$STAGE"/build/web/* docs/
echo "Done: web build copied to docs/"