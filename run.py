import os
import subprocess
import platform

def activate_venv():
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate")
    else:
        return os.path.join("venv", "bin", "activate")

def run_flask_app():
    from app import create_app
    from app.config import Config
    app = create_app()

    if Config.DEBUG:
        print("Running in debug mode...")
        app.run(debug=True) 
    else:
        print("Running in production mode...")
        if platform.system() == "Windows":
            from waitress import serve
            serve(app, host="0.0.0.0", port=5000)
        else:
            subprocess.call(f'gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"', shell=True)

if __name__ == "__main__":
    venv_activation = activate_venv()

    if platform.system() == "Windows":
        subprocess.call(f'start cmd /K "{venv_activation} && python -c \"from run import run_flask_app; run_flask_app()\""', shell=True)
    else:
        subprocess.call(f'source {venv_activation} && python -c "from run import run_flask_app; run_flask_app()"', shell=True, executable='/bin/bash')
