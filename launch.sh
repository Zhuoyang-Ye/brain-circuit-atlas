#!/usr/bin/env bash
# Quick launcher for Brain Circuit Atlas with Python backend
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PORT=8765
echo "Starting Brain Circuit Atlas backend on http://127.0.0.1:$PORT/ ..."
python3 backend/server.py $PORT &
SERVER_PID=$!

trap "kill $SERVER_PID 2>/dev/null" EXIT

sleep 0.8
if command -v open >/dev/null 2>&1; then
    open "http://127.0.0.1:$PORT/"
fi

echo "Brain Circuit Atlas is running. Press Ctrl+C to stop."
wait $SERVER_PID
