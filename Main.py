import subprocess
import os
import datetime
import json
import Timer

config = {"hostname": "", "username": "", "password": "", "accounts": [
    ""], "completed": "{}".format(datetime.datetime.today()), "server_directory": "/backup", "local_directory": "backup", "frequency": "3600", "backup_frequency": "", "backup_range": [2, 23], "pattern": "cpmove-ACCOUNT", "extension": "tar.gz"}


def main():
    while True:
        user_input = input("Standard (s) or Config(c) -> ")
        if user_input == "s":
            if os.path.exists('config.json'):
                subprocess.call(['python.exe', 'Timer.py'])
            else:
                print('Creating config file')
                with open('config.json', 'w') as f:
                    json.dump(config, f)
        elif user_input == "c":
            if os.path.exists('config.json'):
                Timer.configurator()
            else:
                print('Creating config file')
                with open('config.json', 'w') as f:
                    json.dump(config, f)


if __name__ == "__main__":
    main()
