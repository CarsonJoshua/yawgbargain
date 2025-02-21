import os
import subprocess

# Activate the virtual environment
activate_venv = os.path.join('venv', 'bin', 'activate')
subprocess.call(f'source {activate_venv} && gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"', shell=True, executable='/bin/bash')
