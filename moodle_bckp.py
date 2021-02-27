#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import os
import errno
import sys 
import getopt
import logging
import fnmatch

# Logging

# Logging formatter supporting colored output
# Credits: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

# Setup logging
def setup_logging(console_log_output, console_log_level, console_log_color, logfile_file, logfile_log_level, logfile_log_color, log_line_template):

    # Create logger
    logger = logging.getLogger()

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    console_log_output = console_log_output.lower()
    if (console_log_output == "stdout"):
        console_log_output = sys.stdout
    elif (console_log_output == "stderr"):
        console_log_output = sys.stderr
    else:
        print("Failed to set console output: invalid output: '%s'" % console_log_output)
        return False
    console_handler = logging.StreamHandler(console_log_output)

    # Set console log level
    try:
        console_handler.setLevel(console_log_level.upper()) # only accepts uppercase level names
    except:
        print("Failed to set console log level: invalid level: '%s'" % console_log_level)
        return False

    # Create and set formatter, add console handler to logger
    console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create log file handler
    try:
        logfile_handler = logging.FileHandler(logfile_file)
    except Exception as exception:
        print("Failed to set up log file: %s" % str(exception))
        return False

    # Set log file log level
    try:
        logfile_handler.setLevel(logfile_log_level.upper()) # only accepts uppercase level names
    except:
        print("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
        return False

    # Create and set formatter, add log file handler to logger
    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)

    # Success
    return True

def process_retention(retention_policy):
    "This function processes retention policy parameters"
    retention_list = str.split(retention_policy,sep=",",maxsplit=5)
    return(retention_list)

#import gzip
 #from sh import pg_dump

def main():

    usage = str(sys.argv[0]) + " [-o  filename, --output=filename]"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"ho:l:f:d:r:",\
            ['help', 'output=', 'log-level=', 'log-file=', 'backup-directory=','retention='])
    except getopt.GetoptError as option_error:
        print(option_error)
        print(usage)
        sys.exit(2)

    # Default Parameters
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    backup_dir = Path(os.path.expanduser("~")).joinpath("backup")
    output_file = Path(backup_dir).joinpath(script_name + ".tgz")
    log_file = os.devnull
    log_verbose = 0
    historic = False
    retention_policy = [100,100,100,100,100] # 100t 100d 100w 100m 100y

    # Variables
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%m")
    # Reverse date_obj_from_string = datetime.datetime.strptime(date_time_str, '%Y-%m-%d_%H-%m)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ('-o', '--output'):
            output_file = arg
        elif opt in ( '-l', '--log-level'):
            log_verbose = int(arg)
        elif opt in ( '-f', '--log-file'):
            log_file = arg
        elif opt in ( '-d', '--backup-directory'):
            backup_dir = arg
        elif opt in ( '-r', '--retention'):
            historic = True
            retention_policy = arg
            
    # Setup logging
    if log_verbose == 1:
        if (not setup_logging(console_log_output="stdout", console_log_level="critical", console_log_color=True,
                            logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                            log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    elif log_verbose == 2:
        if (not setup_logging(console_log_output="stdout", console_log_level="error", console_log_color=True,
                    logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    elif log_verbose == 3:
        if (not setup_logging(console_log_output="stdout", console_log_level="warning", console_log_color=True,
                    logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    elif log_verbose == 4:
        if (not setup_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                    logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    elif log_verbose == 5:
        if (not setup_logging(console_log_output="stdout", console_log_level="debug", console_log_color=True,
                    logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    else:
        if (not setup_logging(console_log_output="stdout", console_log_level="info", console_log_color=True,
                    logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1

    logging.info('Backup script starting')
    logging.debug("Backup Directory: " + str(backup_dir))
    logging.debug("Backup File: " + str(output_file))
    if log_file != os.devnull:
        logging.debug("Log File: " + str(log_file))
    logging.debug("Log Level: " + str(log_verbose))

   # Setup Backup directory
    logging.info("Backup will be output to a compress file in directory: "+ str(backup_dir))
    if not os.path.exists(backup_dir):
        logging.debug("Directory set for backup does not exists")
        historic = False
        try: 
            os.makedirs(backup_dir)
            logging.debug("Creating directory: " + str(backup_dir))
        except OSError as e:
            logging.error("Error creating directory: " + e.strerror)
            raise

    if historic == True:
        file_history = fnmatch.filter(os.listdir(backup_dir), '*.tgz')
    logging.debug(str(date_time))
    logging.debug(process_retention(retention_policy))

    #if output_file != None:
    #    backup_dir = Path(output_file).parent.absolute()
    #else:
    #    backup_dir = Path(os.path.expanduser("~")).absolute()
    #    logging.warning("Backup file not set, backup to HOME directory")
    #logging.debug('Backup will be output to a compress file in directory: ' + str(backup_dir))

    # Starting setup
    ## Creating backup directory
    #try:
    #    os.makedirs(backup_dir)
    #    print("Creating backup directory in root")
    #except OSError as e:
    #    if e.errno != errno.EEXIST:
    #        raise

    ## test command
    #with gzip.open('backup.gz', 'wb') as f:
    #  pg_dump('-h', 'localhost', '-U', 'postgres', '-F c' , ‘my_dabatase’, _out=f)
    logging.info('Backup script finished')

if __name__ == "__main__":
    main()