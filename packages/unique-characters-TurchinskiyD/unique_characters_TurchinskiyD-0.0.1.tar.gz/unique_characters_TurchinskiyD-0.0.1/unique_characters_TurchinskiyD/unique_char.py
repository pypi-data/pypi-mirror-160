from functools import lru_cache
import argparse


class LoadFileException(Exception):
    pass


@lru_cache()
def unique_characters(txt):
    assert isinstance(txt, str), "На вход должна передаваться строка"
    count = len([elem for elem in txt if txt.count(elem) == 1])
    return count


def create_parser():
    parser = argparse.ArgumentParser(description="Работа функции")
    parser.add_argument('-s', '--string', help='Ввод строки')
    parser.add_argument('-f', '--file', type=str, help='Загружаем файл')  #
    return parser


def processing_parser(parser):
    args = parser.parse_args()
    return args


def load_file(file_name):
    try:
        with open(file_name, "r") as file:
            str_in_file = file.read()
        return str_in_file
    except (FileNotFoundError, TypeError, IOError, UnicodeDecodeError) as e:
        raise LoadFileException


def file_check(pars_args):
    if pars_args.file:
        try:
            return unique_characters(load_file(args.file))
        except LoadFileException as e:
            print("Ошибка обработки файла")
    elif args.string:
        return unique_characters(args.string)


if __name__ == "__main__":

    args = processing_parser(create_parser())
    file_check(args)