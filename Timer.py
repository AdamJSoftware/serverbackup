import time
import datetime
import json
import Engine
import os
import shutil
from threading import Thread
import sys
from dateutil import parser


def config_read():
    with open('config.json', 'r') as f:
        return json.load(f)


def config_write(data):
    with open('config.json', 'w') as f:
        json.dump(data, f)


def backup():
    with open('config.json', 'r') as f:
        config = config_read()
        if config['hostname'] and config['username'] and config['password'] != '':
            x = datetime.datetime.today(
            ) - parser.parse(str(config['completed']))
            if int(x.days) >= int(config['backup_frequency']):
                try:
                    Engine.main(config)
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("Error: {} at line {}".format(
                        e, exc_tb.tb_lineno))
                max_date = datetime.datetime.today(
                ) - datetime.timedelta(days=int(config['local_backup_amount']))
                max_date = f'{max_date.year}-{max_date.month}-{max_date.day}'
                all_backups = []
                if (config['path_option'] == "a"):
                    directory = config['absolute_path']
                else:
                    directory = os.path.join(
                        os.getcwd(), config['relative_path'])
                for item in os.listdir(directory):
                    try:
                        if item < max_date:
                            shutil.rmtree(os.path.join(
                                directory, item))
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


class Main(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            backup()


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
                  "/absolute -> Set the absolute path\n"
                  "/relative -> Set the relative path\n"
                  "/a -> Set default path to absolute\n"
                  "/r -> Set default path to relative\n"
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
        elif user_input == "/absolute":
            config = config_read()
            new_input = input(
                "Please enter the absolute folder location -> ")
            config['absolute_path'] = new_input
            config_write(config)
        elif user_input == "/relative":
            config = config_read()
            new_input = input(
                "Please enter the relative folder location -> ")
            config['relative_path'] = new_input
            config_write(config)
        elif user_input == "/r":
            config = config_read()
            config['path_option'] = 'r'
            config_write(config)
        elif user_input == "/a":
            config = config_read()
            config['path_option'] = 'a'
            config_write(config)
        elif user_input == "/config":
            config = config_read()
            for item in config:
                print('{} - {}'.format(item, config[item]))
        elif user_input == "/backup":
            backup()
        elif user_input == "/restart":
            os._exit(0)


def configurator():
    main()


if __name__ == "__main__":
    main_thread = Main()
    main_thread.start()
    main()
