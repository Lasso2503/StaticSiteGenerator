#!/bin/bash
echo "Running main.sh script..."
echo "python3 src/main.py"
python3 src/main.py
python server.py --dir public
