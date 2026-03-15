#!/bin/bash
set -e

python3 ./JobUpdates/linkedIn_getJobUpdate.py
python3 ./JobUpdates/parseHTMLtoTxt.py