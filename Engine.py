import pysftp
import os
import datetime
from datetime import timedelta
import json
import sys
import time
from stat import *
from threading import Thread


def main(config):
    print('CONNECTING')
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(config['hostname'], username=config['username'], password=config['password'], cnopts=cnopts) as connection:
            if config['next_day'] == "True":
                today = datetime.datetime.today() - timedelta(days=1)
                today_date = datetime.date.today() - timedelta(days=1)
            else:
                today = datetime.datetime.today()
                today_date = datetime.date.today()
            print('SUCCESS CONNECTING')
            directory = config['server_directory'] + "/" + \
                str(today_date) + "/" + 'accounts'
            print(directory)
            connection.chdir(directory)
            print(connection.listdir())
            for account in config['accounts']:
                try:
                    if (config['path_option'] == "a"):
                        directory = config['absolute_path']
                    else:
                        directory = config['relative_path']
                    if not os.path.exists(os.path.join(directory, str(today_date), account)):
                        os.makedirs(os.path.join(directory, str(
                            today_date), account))
                    pattern = config['pattern']
                    pattern = pattern.replace('ACCOUNT', account)
                    localpath = os.path.join(directory, str(
                        today_date), account, f'{account}-{today.day}.{config["extension"]}')
                    print(f'Saving to: {localpath}')
                    remotepath = f'{pattern}.{config["extension"]}'
                    print(f'Pulling from: {remotepath}')
                    print(connection.lstat(remotepath).st_size)
                    loading_bar = LoadingBar(
                        connection.lstat(remotepath).st_size, localpath)
                    loading_bar.start()
                    connection.get(remotepath=remotepath,
                                   localpath=localpath, )
                    time.sleep(1)
                    print('')
                    print('[SUCCESSFULY FINISHED DOWNLOADING]')
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("Engine.py Error: {} at line {}".format(
                        e, exc_tb.tb_lineno))
                    print(f"Couldn't download {account}")
            print('Backing up server files')
            directory = config['server_directory'] + \
                "/" + str(today_date)
            connection.chdir(directory)
            if (config['path_option'] == "a"):
                localpath = os.path.join(
                    config['absolute_path'], str(today_date))
            else:
                localpath = os.path.join(
                    config['relative_path'], str(today_date))
            if not os.path.exists(localpath):
                os.mkdir(localpath)
            connection.get_r(config['system_backup_files'], localpath)
            print('[COMPLETED SYSTEM FILES DOWNLOAD]')
            directory = os.path.join(
                config['server_directory'], str(today_date))
            connection.chdir(config['server_directory'])
            print('REMOVING DIRECTORY')
            connection.execute(f'rm -rf {directory}')
            print('DIRECTORY REMOVED')
            config['completed'] = str(today)
            config_write(config)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Engine.py Error: {} at line {}".format(e, exc_tb.tb_lineno))


class LoadingBar(Thread):
    def __init__(self, file_size, local_path):
        Thread.__init__(self)
        self.file_size = file_size
        self.local_path = local_path

    def run(self):
        time.sleep(1)
        while os.path.getsize(self.local_path) <= self.file_size:
            ratio = os.path.getsize(self.local_path) / self.file_size
            string = ''
            for l in range(int(ratio*20)):
                string = string + '='
            empty = 20 - len(string)
            empty_string = ''
            for j in range(empty):
                empty_string = empty_string + '_'
            percentage = '{:.2f}'.format(round(ratio*100, 2))
            print('[{}{}] {}'.format(
                string, empty_string, percentage) + "%", end='\r')
            if os.path.getsize(self.local_path) == self.file_size:
                print('')
                return
            time.sleep(.5)


def config_write(data):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)
