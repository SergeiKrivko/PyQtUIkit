import argparse
import importlib
import os

import PyQtUIkit.core._version as version
from PyQtUIkit.themes.local import KitLocal

LANGUAGES = dict()
_translator = None


def init_googletrans():
    try:
        from googletrans import Translator, LANGUAGES as LANGS

        global _translator
        _translator = Translator()
        global LANGUAGES
        LANGUAGES = LANGS
    except ImportError:
        print("googletrans is not installed.\nPlease install it with `pip install googletrans==3.1.0a0`")
        exit(0)


def translate(text, dest):
    return _translator.translate(text, dest=dest).text


def import_module(path):
    import sys
    sys.path.insert(0, os.path.dirname(path))
    res = importlib.import_module(os.path.basename(path).split('.')[0])
    sys.path.pop(0)
    return res


def translate_to_lang(filename, lang: str, rewrite=False):
    src_local = import_module(filename).local

    dst_local = None
    if not rewrite:
        try:
            dst_local = import_module(f"{os.path.dirname(filename)}/{lang}.py").local
        except ImportError:
            pass
        except AttributeError:
            pass
    if dst_local is None:
        dst_local = KitLocal(lang, translate(LANGUAGES[lang].capitalize(), lang), dict())

    print(f"Translating to {lang.capitalize()}...")
    with open(f"{os.path.dirname(filename)}/{lang}.py", mode='w', encoding='utf-8') as f:
        f.write(f"from PyQtUIkit.themes.local import KitLocal\n\n"
                f"local = KitLocal('{lang}', '{dst_local.name}', {{\n")
        for key, item in src_local.items():
            try:
                f.write(f"    '{key}': \"{dst_local.get(key)}\",\n")
            except Exception:
                f.write(f"    '{key}': \"{translate(item, lang)}\",\n")
        f.write("})\n")


def main():
    init_googletrans()

    _parser = argparse.ArgumentParser(prog="PyQtUIkit auto translator")

    _parser.add_argument('filename', help="Путь к файлу")
    _parser.add_argument('langs', nargs='*', help="Код(ы) языка(ов)")
    _parser.add_argument('--rewrite', help="При использовании полностью перезаписывает конечный файл.",
                         action='store_true')
    _parser.add_argument('-v', '--version', action='version', version=f"{version.VERSION}")

    args = _parser.parse_args()

    for lang in args.langs:
        translate_to_lang(args.filename, lang, rewrite=args.rewrite)


if __name__ == '__main__':
    main()
