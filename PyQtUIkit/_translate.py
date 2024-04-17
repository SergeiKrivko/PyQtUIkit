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


def get_exists_langs(filename):
    if not filename.endswith('.py'):
        filename += '.py'
    for el in os.listdir(os.path.dirname(filename)):
        if el.endswith('.py') and el != os.path.basename(filename):
            yield el[:-3]


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
    _parser = argparse.ArgumentParser(prog="PyQtUIkit auto translator")

    _parser.add_argument('filename', help="Путь к файлу")
    _parser.add_argument('langs', nargs='*', help="Код(ы) языка(ов)")
    _parser.add_argument('--rewrite', help="При использовании полностью перезаписывает конечный файл.",
                         action='store_true')
    _parser.add_argument('--update', help="Обновить все файлы локализаций в той же папке, что и filename,"
                                          "кроме самого filename", action='store_true')
    _parser.add_argument('-v', '--version', action='version', version=f"{version.VERSION}")

    args = _parser.parse_args()

    init_googletrans()

    for lang in args.langs:
        translate_to_lang(args.filename, lang, rewrite=args.rewrite)

    if args.update:
        for lang in get_exists_langs(args.filename):
            if lang not in args.langs and lang in LANGUAGES:
                translate_to_lang(args.filename, lang, rewrite=args.rewrite)


if __name__ == '__main__':
    main()
