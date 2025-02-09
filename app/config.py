import configparser

config = configparser.ConfigParser()
config.read("config.ini")

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config['database']['dbname']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config["database"]["SQLALCHEMY_TRACK_MODIFICATIONS"]
    SECRET_KEY = "supersecretkey"  # Replace this with an env variable later
