import pysftp
import os
import datetime

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


def main(config):
    with pysftp.Connection(config['hostname'], username=config['username'], password=config['password'], cnopts=cnopts) as connection:
        connection.chdir(config['server_directory'])
        print(connection.listdir())
        for account in config['accounts']:
            if os.path.exists(os.path.join(config['local_directory'], account)):
                pattern = config['pattern']
                pattern = pattern.replace('ACCOUNT', account)
                with open(os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension'])) as f:
                    pass
                connection.get('{}.{}'.format(pattern, config['extension']),
                               localpath=os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension']))
            else:
                os.mkdir(os.path.join(config['local_directory'], account))
                pattern = config['pattern']
                pattern.replace('ACCOUNT', account)
                with open(os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension'])) as f:
                    pass
                connection.get('{}.{}'.format(pattern, config['extension']),
                               localpath=os.path.join(config['local_directory'], account, '{}-{}.{}').format(account, datetime.datetime.today().day, config['extension']))
