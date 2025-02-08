import configparser, subprocess

config = configparser.ConfigParser()
config.read("config.ini")

subprocess.run(f'PGPASSWORD="{config["database"]["password"]}" psql -h {config["database"]["host"]} -U {config["database"]["user"]} -d {config["database"]["dbname"]}', shell=True)