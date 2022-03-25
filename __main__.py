#!/usr/bin/python

# Stewart Francis
# SRE Programming Tests 

"""
   depend.__main__

   This is the command line interface for the depend tool.

   Valid Commands are:

   DEPEND item1 item2      -- Package item1 depends on packge item2 (can be more than a single package)
   INSTALL item1           -- Installs item1 and any of the packages that depend on it
   REMOVE item1            -- Removes item1 and if possible packages required by item1
   LIST                    -- Lists the names of all currently installed packages
   END                     -- Ends interactive input when used in a line by itself
"""
import sys
from dependcli import DependCLI

if __name__ == "__main__":
   cli = DependCLI()

   for line in sys.stdin:
      if "END" == line.rstrip():
         break
      cli.parse_command(line.rstrip())


   
