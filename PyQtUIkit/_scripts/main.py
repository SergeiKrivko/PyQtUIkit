import argparse
from sys import argv

from PyQtUIkit._scripts.project_init import init_project
from PyQtUIkit._scripts.icons import main as run_icons


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', choices=['run', 'init', 'icons', 'translate'])

    args = parser.parse_args(argv[1:2])

    match args.command:
        case 'run':
            pass
        case 'init':
            init_project(argv[2:])
        case 'icons':
            run_icons(argv[2:])
        case 'translate':
            pass


if __name__ == '__main__':
    main()
