import pysftp
import os
import datetime
import time
from stat import *
from threading import Thread

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


def main(config):
    with pysftp.Connection(config['hostname'], username=config['username'], password=config['password'], cnopts=cnopts) as connection:
        directory = config['server_directory'] + "/" + \
            str(datetime.date.today()) + "/" + 'accounts'
        print(directory)
        connection.chdir(directory)
        print(connection.listdir())
        for account in config['accounts']:
            if not os.path.exists(os.path.join(config['local_directory'], str(datetime.date.today()), account)):
                os.makedirs(os.path.join(
                    config['local_directory'], str(datetime.date.today()), account))
            pattern = config['pattern']
            pattern = pattern.replace('ACCOUNT', account)
            localpath = os.path.join(config['local_directory'], str(datetime.date.today()), account, '{}-{}.{}').format(
                account, datetime.datetime.today().day, config['extension'])
            print('Saving to: {}'.format(localpath))
            remotepath = '{}.{}'.format(pattern, config['extension'])
            print('Pulling from: {}'.format(remotepath))
            print(connection.lstat(remotepath).st_size)
            loading_bar = LoadingBar(
                connection.lstat(remotepath).st_size, localpath)
            loading_bar.start()
            connection.get(remotepath=remotepath, localpath=localpath)
            time.sleep(1)
            print('')
            print('[SUCCESSFULY FINISHED DOWNLOADING]')
        print('Backing up server files')
        directory = config['server_directory'] + "/" + \
            str(datetime.date.today())
        connection.chdir(directory)
        localpath = os.path.join(config['local_directory'], str(
            datetime.date.today()))
        if not os.path.exists(localpath):
            os.mkdir(localpath)

        connection.get_r(config['system_backup_files'], localpath)
        print('[COMPLETED SYSTEM FILES DOWNLOAD]')


class LoadingBar(Thread):
    def __init__(self, file_size, local_path):
        Thread.__init__(self)
        self.file_size = file_size
        self.local_path = local_path

    def run(self):
        time.sleep(1)
        while os.path.getsize(self.local_path) <= self.file_size:
            ratio = os.path.getsize(self.local_path) / self.file_size
            # print(ratio, end='\r')
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
            time.sleep(.5)
        print('')
        return
