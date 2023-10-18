#!/bin/bash
# flask settings
export FLASK_APP=/opt/puc-prompter
export FLASK_DEBUG=0

cd /opt/puc-prompter
source /opt/venv/bin/activate && python3.7 app.py
