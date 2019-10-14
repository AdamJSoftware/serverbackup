import time
import datetime
import json
import Engine
import os
from threading import Thread
import sys


def config_read():
    with open('config.json', 'r') as f:
        return json.load(f)


def config_write(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            with open('config.json', 'r') as f:
                config = config_read()
            if config['hostname'] and config['username'] and config['password'] != '':
                if (datetime.datetime.today().day - datetime.datetime.strptime(config['completed'], '%Y-%m-%d %H:%M:%S.%f').day >= int(config['backup_frequency'])):
                    try:
                        Engine.main(config)
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print("Error: {} at line {}".format(
                            e, exc_tb.tb_lineno))
                    time.sleep(int(config['frequency']))
                else:
                    time.sleep(int(config['frequency']))
            else:
                print('Please set hostname, username and password')
                time.sleep(int(config['frequency']))


def main():
    while True:
        user_input = input('-> ')
        if user_input == '/help':
            print("/account_list -> Lists all acounts\n"
                  "/account_add -> Adds an account\n"
                  "/account_remove -> Removes an account\n"
                  "/backup -> Backups a specifc(s) account\n"
                  "/backup_all -> Backups all accounts\n"
                  "/backup_time -> Changes backup frequency\n"
                  "/hostname -> Changes server hostname\n"
                  "/username -> Changes server username\n"
                  "/password -> Changes server password\n"
                  "/server_directory -> Changes server backup directory\n"
                  "/local_directory -> Changes local backup directory\n"
                  "/backup_frequency -> Changes how often the system downloads backup files\n"
                  "/backup_range -> Changes when backups are allowed to occur\n"
                  "/pattern -> Change what the server backup file pattern\n"
                  "/extension -> Changes the extension of the backup file\n"
                  "/config -> Prints entire config file\n"
                  "/restart -> Restart the program")
        elif user_input == "/account_list":
            config = config_read()
            for account in config['accounts']:
                print('\t - {}'.format(account))
        elif user_input == "/account_add":
            config = config_read()
            new_input = input("Please type in the name of the account -> ")
            config['accounts'].append(new_input)
            config_write(config)
        elif user_input == "/account_remove":
            config = config_read()
            for account in config['accounts']:
                print('\t - {}'.format(account))
            new_input = input(
                "Please type in the name of the account you want to remove -> ")
            config['accounts'].remove(new_input)
            config_write(config)
        elif user_input == "/backup_time":
            config = config_read()
            new_input = input(
                "Please type in the new backup check frequency (seconds) -> ")
            config['frequency'] = new_input
            config_write(config)
        elif user_input == "/hostname":
            config = config_read()
            new_input = input(
                "Please type in the new hostname -> ")
            config['hostname'] = new_input
            config_write(config)
        elif user_input == "/username":
            config = config_read()
            new_input = input(
                "Please type in the new username -> ")
            config['username'] = new_input
            config_write(config)
        elif user_input == "/password":
            config = config_read()
            new_input = input(
                "Please type in the new password -> ")
            config['password'] = new_input
            config_write(config)
        elif user_input == "/server_directory":
            config = config_read()
            new_input = input(
                "Please type in the new server directory -> ")
            config['server_directory'] = new_input
            config_write(config)
        elif user_input == "/local_directory":
            config = config_read()
            new_input = input(
                "Please type in the new local directory -> ")
            config['local_directory'] = new_input
            config_write(config)
        elif user_input == "/backup_frequency":
            config = config_read()
            new_input = input(
                "Please type in the new backup frequency (days) -> ")
            config['backup_frequency'] = new_input
            config_write(config)
        elif user_input == "/backup_range":
            config = config_read()
            start = input(
                "Please enter start (24 hour format) -> ")
            end = input("Please enter end (24 hour format) -> ")
            config['backup_range'] = [start, end]
            config_write(config)
        elif user_input == "/extension":
            config = config_read()
            new_input = input(
                "Please enter the file extension (ex: tar.gz) -> ")
            config['extension'] = new_input
            config_write(config)
        elif user_input == "/pattern":
            config = config_read()
            new_input = input(
                "Please enter the file pattern (cpmove-ACCOUNT) -> ")
            config['pattern'] = new_input
            config_write(config)
        elif user_input == "/backup_all":
            config = config_read()
            try:
                Engine.main(config)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("Error: {} at line {}".format(
                    e, exc_tb.tb_lineno))
        elif user_input == "/config":
            config = config_read()
            for item in config:
                print('{} - {}'.format(item, config[item]))
        elif user_input == "/restart":
            os._exit(0)


def configurator():
    main()


if __name__ == "__main__":
    main_thread = Main()
    main_thread.start()
    main()
