import sys
import os
import shutil

from cheat import sheets
from cheat.utils import die, open_with_editor

def copy(current_sheet_path, new_sheet_path):
    """ Copies a sheet to a new path """

    # attempt to copy the sheet to DEFAULT_CHEAT_DIR
    try:
        shutil.copy(current_sheet_path, new_sheet_path)

    # fail gracefully if the cheatsheet cannot be copied. This can happen if
    # DEFAULT_CHEAT_DIR does not exist
    except IOError:
        die('Could not copy cheatsheet for editing.')


def create_or_edit(sheet):
    """ Creates or edits a cheatsheet """

    # if the cheatsheet does not exist
    if not exists(sheet):
        create(sheet)

    # if the cheatsheet exists but not in the default_path, copy it to the
    # default path before editing
    elif exists(sheet) and not exists_in_default_path(sheet):
        copy(path(sheet), os.path.join(sheets.default_path(), sheet))
        edit(sheet)

    # if it exists and is in the default path, then just open it
    else:
        edit(sheet)


def create(sheet):
    """ Creates a cheatsheet """
    new_sheet_path = os.path.join(sheets.default_path(), sheet)
    open_with_editor(new_sheet_path)


def edit(sheet):
    """ Opens a cheatsheet for editing """
    open_with_editor(path(sheet))


def exists(sheet):
    """ Predicate that returns true if the sheet exists """
    return sheet in sheets.get() and os.access(path(sheet), os.R_OK)


def exists_in_default_path(sheet):
    """ Predicate that returns true if the sheet exists in default_path"""
    default_path_sheet = os.path.join(sheets.default_path(), sheet)
    return sheet in sheets.get() and os.access(default_path_sheet, os.R_OK)


def is_writable(sheet):
    """ Predicate that returns true if the sheet is writeable """
    return sheet in sheets.get() and os.access(path(sheet), os.W_OK)


def path(sheet):
    """ Returns a sheet's filesystem path """
    return sheets.get()[sheet]


def read(sheet):
    """ Returns the contents of the cheatsheet as a String """
    if not exists(sheet):
        die('\033[1;31mNo\033[0m cheatsheet found for \033[1;31m' + sheet + '\033[0m')

    with open(path(sheet)) as cheatfile:
        return cheatfile.read()

def remove(sheet, default="yes"):
    """Ask a yes/no/quit sheet via raw_input() and return their answer.

    "sheet" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no", "quit" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes", "no" or "quit".
    """

    if not exists(sheet):
        die('\033[1;31mNo\033[0m cheatsheet found for \033[1;31m' + sheet + '\033[0m')

    sheet = sheets.get()[sheet]

    valid = {"yes":"yes",   "y":"yes",    "ye":"yes",
             "no":"no",     "n":"no",
             "quit":"quit", "qui":"quit", "qu":"quit", "q":"quit"}
    if default == None:
        prompt = " [y/n/q] "
    elif default == "yes":
        prompt = " [Y/n/q] "
    elif default == "no":
        prompt = " [y/N/q] "
    elif default == "quit":
        prompt = " [y/n/Q] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while 1:
        sys.stdout.write(sheet + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            print("Delete\033[1;31m %s \033[0mfile " % sheet)
            os.remove(sheet)
            return default
        elif choice in valid.keys():
            print("Delete\033[1;31m %s \033[0mfile " % sheet)
            os.remove(sheet)
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes', 'no' or 'quit'.\n")



