import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Config:

    # Flask settings
    DEBUG = config.get("flask", "debug", fallback=True) 
    HOST = config.get("flask", "host", fallback="0.0.0.0")
    PORT = int(config.get("flask", "port", fallback=5000))

    # DB settings
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config['database']['dbname']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config["database"]["SQLALCHEMY_TRACK_MODIFICATIONS"]
    SECRET_KEY = "supersecretkey"  # Replace this with an env variable later
