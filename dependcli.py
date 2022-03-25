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
from depend import Depend

class DependCLI:
   depend = Depend()
   commandalias = {}

   def __init__(self):
      self.commandalias = {"DEPEND": self.handle_depend, "INSTALL": self.handle_install, "REMOVE": self.handle_remove, "LIST": self.handle_list}

   def handle_depend(self, args):
      # The package is the first entry, the remaining are the dependencies
      self.depend.depend(args.pop(0), args)

   def handle_install(self, args):
      # Should only be a single arg
      self.depend.install(args[0])

   def handle_remove(self, args):
      # Same, single arg
      self.depend.remove(args[0])
   
   def handle_list(self, args):
      # No args, but we'll keep the same sig for sanity
      self.depend.list()

   def parse_command(self, command):
      # split by space
      args = command.split(" ")
      
      # first is our command
      cmd = args.pop(0)

      if cmd in self.commandalias:
         self.commandalias[cmd](args)
      else:
         print(f"{cmd} is not a valid command.")

if __name__ == "__main__":
   cli = DependCLI()

   for line in sys.stdin:
      if "END" == line.rstrip():
         break
      cli.parse_command(line.rstrip())


   
