from distutils.core import setup
import py2exe, sys

filename = sys.argv[1]

print filename

sys.argv.pop()

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'dll_excludes': [ "mswsock.dll", "powrprof.dll" ]}},
    console = [{'script': filename}],
    zipfile = None,	
)