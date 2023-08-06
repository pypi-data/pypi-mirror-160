# import faulthandler
# faulthandler.enable()

import subprocess
import sys
import argparse
from argparse import RawTextHelpFormatter
import logging

log = logging.getLogger(__name__)

from partis.utils import (
  init_logging,
  HINT_LEVELS_DESC )

verbosity_help = ""

for k,v in HINT_LEVELS_DESC.items():
  verbosity_help += f"'{k}' : {v}\n"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-t", "--theme",
    type = str,
    default = 'light',
    help = "gui theme { 'light', 'dark' }." )

  parser.add_argument( "-i", "--init",
    type = str,
    default = "",
    help = "Initialization file" )

  parser.add_argument( "-l", "--log",
    type = str,
    default = None,
    help = "Directs log output to the given log file, in addition to stdout" )

  parser.add_argument( "-v", "--verbosity",
    type = str,
    default = 'error',
    help = "Log verbosity: (default = 'error')\n" + verbosity_help )

  parser.add_argument('init',
    type = str,
    default = None,
    nargs='?',
    help = "File or directory to open initially" )

  return parser


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def main():

  parser = argument_parser( )
  args = parser.parse_args( )

  init_logging(
    level = args.verbosity,
    filename = args.log )


  from partis.view import (
    MainWindow,
    Manager )

  app_manager = Manager(
    main_window_class = MainWindow,
    theme = args.theme,
    init_file = args.init )

  return app_manager.run()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == "__main__":
  exit( main() )
