#!/usr/bin/env zsh
source env/bin/activate
python app/main.py
cd public && python -m http.server 8888