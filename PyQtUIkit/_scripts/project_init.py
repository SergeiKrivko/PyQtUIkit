import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--name', type=str, default='New Project', help='Name of project')
parser.add_argument('-p', '--path', type=str, default='.', help='Name of project')

args: argparse.Namespace = argparse.Namespace()


def path(name):
    return os.path.join(args.path, name)


def init_project(argv):
    global args
    args = parser.parse_args(argv)

    os.makedirs(args.path, exist_ok=True)
    with open(path('project.py'), 'w') as f:
        f.write(f"""from PyQtUIkit import KitApplication

from src.main_window import MainWindow


app = KitApplication(
    name={repr(args.name)},
    version='0.0.1',
    window=MainWindow,
    styles=['assets/styles/main.xml'],
    icons_path='assets/icons',
    locale_path='assets/locale',
)
""")
    os.makedirs(path('src'), exist_ok=True)
    os.makedirs(path('assets/icons'), exist_ok=True)
    os.makedirs(path('assets/styles'), exist_ok=True)
    os.makedirs(path('assets/locale'), exist_ok=True)
    with open(path('src/main_window.py'), 'w') as f:
        f.write(f"""from PyQtUIkit.widgets import KitMainWindow, KitButton


class MainWindow(KitMainWindow):
    def __init__(self):
        super().__init__(KitButton('Press me!'))

""")
    with open(path('assets/styles/main.xml'), 'w') as f:
        f.write(f"""<?xml version="1.0" encoding="utf-8" ?>
<uikit-style>

</uikit-style>
""")


if __name__ == '__main__':
    init_project()
