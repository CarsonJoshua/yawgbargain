import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Config:

    # Flask settings
    DEBUG = config.getboolean("flask", "debug", fallback=True)
    HOST = config.get("flask", "host", fallback="0.0.0.0")
    PORT = int(config.get("flask", "port", fallback=5000))

    # DB settings
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}/{config['database']['dbname']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config["database"]["SQLALCHEMY_TRACK_MODIFICATIONS"]
    SECRET_KEY = "supersecretkey"


    def __repr__(self):
        return f"<Config ({', '.join(f'{key}={value!r}' for key, value in self.__class__.__dict__.items() if not key.startswith('__'))})>"