# encoding:utf-8
""" Mariner -- A package manager for RingRobotX
Usage:
    mar get-rrx [--script-url=<git_url>]
    mar install <skill_name> [--mirror=<mirror_url>]
    mar uninstall <skill_name>
    mar build [skill_name]
    mar upgrade-all [--mirror=<mirror_url>]
    mar upgrade <skill_name> [--mirror=<mirror_url>]
    mar -h | --help
    mar -v | --version


Options:
    -h --help     Show Help doc.
    -v --version     Show Version.
    --mirror=<mirror_url>     Set a mirror for skills. [default: https://gitee.com/waterflames-team/mariner-mirror/raw/master/]
    --script-url=<git_url>     Set a custom-script for RingRobotX. [default: https://gitee.com/waterflames-team/ring-robot-x/raw/master/install.sh]
"""
import random

import mariner_rrx
from docopt import docopt


def run():
    args = docopt(__doc__, version=mariner_rrx.__version__)
    if args.get("get-rrx"):
        mariner_rrx.get.get(args)
    elif args.get("install"):
        mariner_rrx.install.install(args)
    elif args.get("uninstall"):
        mariner_rrx.uninstall.uninstall(args)
    elif args.get("build"):
        mariner_rrx.build.build(args)
    elif args.get("upgrade"):
        mariner_rrx.upgrade.upgrade(args)
    elif args.get("upgrade-all"):
        mariner_rrx.upgrade.upgrade_all(args)
    else:
        print("Command not found.")


if __name__ == "__main__":
    run()
