from datetime import datetime
from pathlib import Path
import os
import errno
#import gzip

#from sh import pg_dump
# Variables
## Date
date = datetime.now().strftime("%Y-%m-%d")

## Directories
script_dir = Path(__file__).parent.absolute()
backup_dir = Path().absolute().joinpath('backup')

## Files
backup_file = backup_dir.joinpath(str(date)+".tgz")

# Starting setup
## Creating backup directory
try:
    os.makedirs(backup_dir)
    print("Creating backup directory in root")
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

## test command
#with gzip.open('backup.gz', 'wb') as f:
#  pg_dump('-h', 'localhost', '-U', 'postgres', '-F c' , ‘my_dabatase’, _out=f)