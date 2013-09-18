from distutils.core import setup
import py2exe

options = {"py2exe": { # create a compressed zip archive
                      "compressed": 1,
                      "optimize": 2,
                      "excludes": ["Image"],
                      "includes": ["encodings", "encodings.*"],
                          }}

setup(windows=["meeting_helper.py"], options=options,
      data_files=["meeting_helper.rsrc.py", "meeting_helper_displayOnly.rsrc.py", "fwdArrow.jpg", "backArrow.jpg", "unicows.dll"],
)



# use for example as:
#   c:\python24\python setup.py py2exe
#    then "dist" is the distribution directory
