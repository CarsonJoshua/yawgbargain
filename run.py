import os
import subprocess
from app import create_app
from app.config import Config
import platform

app = create_app()

def activate_venv():
    """Returns the appropriate command to activate the virtual environment based on the OS."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate")  # Windows activation script
    else:
        return os.path.join("venv", "bin", "activate")  # Linux/macOS activation script

if __name__ == "__main__":
    if Config.DEBUG:
        print("Running in debug mode...")
        app.run(debug=True)  # Run Flask's built-in server
    else:
        print("Running in production mode...")
        venv_activation = activate_venv()

        if platform.system() == "Windows":
            subprocess.call(f'{venv_activation} && gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"', shell=True)
        else:
            subprocess.call(f'source {venv_activation} && gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"', shell=True, executable='/bin/bash')
