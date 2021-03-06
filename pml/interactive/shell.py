# Copyright (C) 2012 David Rusk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
"""
Runs a customised IPython shell.

Inspired by: 
https://github.com/ingenuitas/SimpleCV/blob/develop/SimpleCV/Shell/Shell.py

@author: drusk
"""

import sys
import webbrowser

from IPython.config.loader import Config
from IPython.frontend.terminal.embed import InteractiveShellEmbed

from pml.interactive.util import no_stdout
from pml.interactive.tutorial import begin_tutorial, get_tutorial_lessons

# Import pml library.  These imports will be available in the shell that 
# is created.
from pml.api import *

def magic_tutorial(self, arg):
    """
    The function called when the 'tutorial' magic is executed.  
    Arg can be used to start up a specific lesson by name instead of the 
    full tutorial from the beginning.  If arg is 'list', a list of tutorial
    lessons is displayed.
    """
    if arg == "":
        begin_tutorial()
    elif arg == "list":
        print "Lessons in the tutorial:"
        print get_tutorial_lessons().keys()
        print ""
        print "To begin at a specific lesson instead of the beginning, "
        print "type 'tutorial <name>' (ex: 'tutorial datasets')"
    else:
        lessons = get_tutorial_lessons()
        if arg in lessons:
            lessons[arg]()
        else:
            print "Unrecognized lesson name: %s" % arg

def magic_docs(self, arg):
    """
    The function called when the 'docs' magic is executed.  IPython requires 
    this function to accept two parameters, even though they are not used in 
    this instance.
    """
    with no_stdout():
        webbrowser.open("http://pml.readthedocs.org/en/latest/index.html")

def setup_shell():
    banner  = "+----------------------------------------------------------------------+\n"
    banner += " PML Shell - built on IPython.\n"
    banner += "+----------------------------------------------------------------------+\n"
    banner += "Commands: \n"
    banner += "\t'tutorial' will begin the interactive tutorial.\n"
    banner += "\t'tutorial list' will display individual lessons in the tutorial.\n"
    banner += "\t'docs' will open up the online documentation in a web browser.\n"
    banner += "\t'exit', 'quit' or press 'CTRL + D' to exit the shell.\n"

    exit_message = "\n* Exiting PML shell, good bye! *\n"
    
    # XXX: this currently only supports IPython version 0.11 or higher!
    config = Config()
    config.PromptManager.in_template = "pml:\\#> "
    config.PromptManager.out_template = "pml:\\#: "
    
    pml_shell = InteractiveShellEmbed(config=config, banner1=banner, 
                                      exit_msg=exit_message)
    
    pml_shell.define_magic("tutorial", magic_tutorial)
    pml_shell.define_magic("docs", magic_docs)
    
    return pml_shell

def run():
    pml_shell = setup_shell()
    sys.exit(pml_shell())

if __name__ == "__main__":
    run()
    