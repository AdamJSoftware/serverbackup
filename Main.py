import subprocess
import os
import datetime
import json
import Timer

config = {"hostname": "", "username": "", "password": "", "accounts": [], "completed": "{}".format(datetime.datetime.today(
)), "server_directory": "/backup", "local_directory": "backup", "frequency": "3600", "backup_frequency": "1", "backup_range": [2, 23], "pattern": "ACCOUNT", "extension": "tar.gz",
    "system_backup_files": "system", "local_backup_amount": "14"}


def main():
    while True:
        user_input = input("Standard (s) or Config(c) -> ")
        if user_input == "s":
            if os.path.exists('config.json'):
                try:
                    subprocess.call(['python', 'Timer.py'])
                except Exception as e:
                    print(e)
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
