#!/bin/sh

curl --proto "=https" --tlsv.12 -H 'Cache-Control: no-cache' -f "https://raw.githubusercontent.com/neerajnangireddy/infer-py-packages/refs/heads/main/ipypk.py" -o ~/.local/bin/ipypk
chmod +x ~/.local/bin/ipypk

