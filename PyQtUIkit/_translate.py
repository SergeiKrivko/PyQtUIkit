import argparse
import importlib
import os

import PyQtUIkit.core._version as version
from PyQtUIkit.themes.locale import KitLocale

_translator = None


def init_googletrans():
    try:
        from translatepy import Translator, Language

        global _translator
        _translator = Translator()
    except ImportError:
        print("translatepy is not installed.\nPlease install it with `pip install translatepy`")
        exit(0)


def translate(text, dest):
    return _translator.translate(text, dest).result


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
    src_locale = import_module(filename).locale

    dst_locale = None
    if not rewrite:
        try:
            dst_locale = import_module(f"{os.path.dirname(filename)}/{lang}.py").locale
        except ImportError:
            pass
        except AttributeError:
            pass
    if dst_locale is None:
        from translatepy import Language
        dst_locale = KitLocale(lang, translate(Language(lang).name, lang).capitalize(), dict())

    print(f"Translating to {lang.capitalize()}...")
    res = ["from PyQtUIkit.themes.locale import KitLocale\n",
           f"locale = KitLocale('{lang}', '{dst_locale.name}', {{"]
    for key, item in src_locale.items():
        try:
            res.append(f"    '{key}': \"{dst_locale.get(key)}\",")
        except Exception:
            res.append(f"    '{key}': \"{translate(item, lang)}\",")
    res.append("})\n")
    with open(f"{os.path.dirname(filename)}/{lang}.py", mode='w', encoding='utf-8') as f:
        f.write('\n'.join(res))


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
            if lang not in args.langs:
                translate_to_lang(args.filename, lang, rewrite=args.rewrite)


if __name__ == '__main__':
    main()
