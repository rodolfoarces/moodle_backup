#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import os
import errno
import sys 
import getopt
import logging

# Logging

# Logging formatter supporting colored output
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
    # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
    # without name argument. This way we can simply use module methods for
    # for logging throughout the script. An alternative would be exporting
    # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
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


#import gzip
 #from sh import pg_dump

def main():

    usage = str(sys.argv[0]) + " [-o  filename, --output=filename]"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"ho:l:f:",['help', 'output=', 'log-level=', 'log-file='])
    except getopt.GetoptError as option_error:
        print(option_error)
        print(usage)
        sys.exit(2)

    # Parameters
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    output_file = None
    log_file = Path(os.path.expanduser("~")).joinpath(script_name + ".log")
    log_verbose = 0

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage)
            sys.exit()
        elif opt in ('-o', '--output'):
            output_file = arg
            print("Setando output: ", output_file)
        elif opt in ( '-l', '--log-level'):
            log_verbose = arg
            print("Setando log_verbose: ", log_verbose)
        elif opt in ( '-f', '--log-file'):
            log_file = arg
            print("Setando log_file: ", log_file)

    # Setup logging
    
    if log_verbose == 0: 
        if (not setup_logging(console_log_output="stdout", console_log_level="warning", console_log_color=True,
                            logfile_file=log_file, logfile_log_level="debug", logfile_log_color=False,
                            log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")):
            print("Failed to setup logging, aborting.")
            return 1
    elif log_verbose == 1:
        if (not setup_logging(console_log_output="stdout", console_log_level="warning", console_log_color=True,
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
        print("No pasa nada")
        #logging.basicConfig(format='[%(created)d] [%(threadName)s] [%(levelname)s] - %(message)s', level=logging.DEBUG)

    # Prueba
    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")

    logging.info('Started')

   # Setup Backup directory
    if output_file != None:
        backup_dir = Path(output_file).parent.absolute()
        
    else:
        backup_dir = Path(os.path.expanduser("~")).absolute()
        logging.warn("Backup file not set, backup to HOME directory")

    #if 
    logging.debug('Backup will be output to a compress file in directory: ' + str(backup_dir))

   
    # Variables
    ## Date
    date = datetime.now().strftime("%Y-%m-%d")

    ## Directories
    script_dir = Path(__file__).absolute()
    

    ## Files
    backup_file = backup_dir.joinpath(str(date)+".tgz")

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
    logging.info('Finished')

if __name__ == "__main__":
    main()