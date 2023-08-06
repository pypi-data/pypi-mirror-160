#!/usr/bin/env python3
"""
This command tries to emulate pylint in order to get pycharm work using flake8
"""
import os
import sys
import argparse
import tempfile
import getpass

PID_FILE='{temp_dir}/{user}_flake8_pid'.format(temp_dir=tempfile.gettempdir(), user=getpass.getuser())

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--output-format")
parser.add_argument("--help-msg")
parser.add_argument("--rcfile")
parser.add_argument("files", nargs="*", default=42)

args = parser.parse_args()
flake8_args = [sys.argv[0], "--format=pycharm"]


def get_flake8_executable_filename():
    script_filename = sys.argv[0]
    script_dir = os.path.dirname(script_filename)
    return os.path.join(script_dir, "flake8")


def ensure_only_one_flake8_instance_is_running():
    if os.path.isfile(PID_FILE):
        with open(PID_FILE) as pid_file:
            old_pid = pid_file.read().strip()
            try:
                os.kill(int(old_pid), 15)
            except ProcessLookupError:
                pass
    pid = os.getpid()
    with open(PID_FILE, 'w') as pid_file:
        pid_file.write(str(pid))


if args.help_msg:
    print("""
    :no-member (E1101): *%s %r has no %r member%s*
    Used when a variable is accessed for an unexistent member. This message
    belongs to the typecheck checker.
    """)  # noqa: WPS421
    sys.exit(0)

if args.output_format != "json":
    # Attempting to call pylint?
    os.execlp("pylint", *sys.argv)  # noqa:S607,S606

if args.rcfile:
    flake8_args.append("--config")
    flake8_args.append(args.rcfile)

flake8_args += args.files

ensure_only_one_flake8_instance_is_running()
os.execv(get_flake8_executable_filename(), flake8_args)  # noqa: S606
