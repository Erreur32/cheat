import os

from cheat import cheatsheets
from cheat.utils import die

def default_path():
    """ Returns the default cheatsheet path """

    # determine the default cheatsheet dir
    default_sheets_dir = os.environ.get('DEFAULT_CHEAT_DIR') or os.path.join('~', '.cheat')
    default_sheets_dir = os.path.expanduser(os.path.expandvars(default_sheets_dir))

    # create the DEFAULT_CHEAT_DIR if it does not exist
    if not os.path.isdir(default_sheets_dir):
        try:
            # @kludge: unclear on why this is necessary
            os.umask(0000)
            os.mkdir(default_sheets_dir)

        except OSError:
            die('Could not create DEFAULT_CHEAT_DIR')

    # assert that the DEFAULT_CHEAT_DIR is readable and writable
    if not os.access(default_sheets_dir, os.R_OK):
        die('The DEFAULT_CHEAT_DIR (' + default_sheets_dir +') is not readable.')
    if not os.access(default_sheets_dir, os.W_OK):
        die('The DEFAULT_CHEAT_DIR (' + default_sheets_dir +') is not writable.')

    # return the default dir
    return default_sheets_dir


def get():
    """ Assembles a dictionary of cheatsheets as name => file-path """
    cheats = {}

    # otherwise, scan the filesystem
    for cheat_dir in reversed(paths()):
        subdirs = []
        for root, dirs, files in os.walk(cheat_dir, topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            subdirs.append(root)

        for subdir in subdirs:
            cheats.update(
                dict([
                    (cheat, os.path.join(subdir, cheat))
                    for cheat in os.listdir(subdir)
                    if not cheat.startswith('.')
                    and not cheat.startswith('__')
                    and not os.path.isdir(os.path.join(subdir, cheat))
                ])
            )


    return cheats


def paths():
    """ Assembles a list of directories containing cheatsheets """
    sheet_paths = [
        default_path(),
        cheatsheets.sheets_dir()[0],
    ]

    # merge the CHEATPATH paths into the sheet_paths
    if 'CHEATPATH' in os.environ and os.environ['CHEATPATH']:
        for path in os.environ['CHEATPATH'].split(os.pathsep):
            if os.path.isdir(path):
                sheet_paths.append(path)

    if not sheet_paths:
        die('The DEFAULT_CHEAT_DIR dir does not exist or the CHEATPATH is not set.')

    return sheet_paths


def list():
    """ Lists the available cheatsheets """
    sheet_list = ''
    pad_length = max([len(x) for x in get().keys()]) + 4
    for sheet in sorted(get().items()):
        sheet_list += sheet[0].ljust(pad_length) + sheet[1] + "\n"
    return sheet_list


def search(term, target_sheet):
    """ Searches all cheatsheets for the specified term.
        Restrict search to target_sheet if given """
    result = ''
    for cheatsheet in sorted(get().items()):
        if target_sheet and target_sheet != cheatsheet[0]:
            continue
        match = ''
#        for line in open(cheatsheet[1]):
        for index, line in enumerate(open(cheatsheet[1])):
            if term in line:
                 match += '[%d]\t\t' % index + line.strip() + '\n'
#                if 'CHEATCOLORS' in os.environ:
#                    line = line.replace(term, '\033[1;31m'+ term +'\033[0m');
#                match += '  ' + line

        if match != '':
            result += cheatsheet[0] + ":\n" + match + "\n"

    return result
