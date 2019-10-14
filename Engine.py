import pysftp
import os
import datetime


def main(config):
    with pysftp.Connection(config['hostname'], username=config['username'], password=config['password']) as connection:
        connection.chdir(config['server_directory'])
        print(connection.listdir())
        for account in config['accounts']:
            if os.path.exists(os.path.join(config['local_directory'], account)):
                pattern = config['pattern']
                pattern = pattern.replace('ACCOUNT', account)
                print(pattern)
                connection.get('{}.{}'.format(pattern, config['extension']),
                               localpath=os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension']))
            else:
                os.mkdir(os.path.join(config['local_directory'], account))
                pattern = config['pattern']
                pattern.replace('ACCOUNT', account)
                connection.get('{}.{}'.format(pattern, config['extension']),
                               localpath=os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension']))


def create_folder():
    pass
