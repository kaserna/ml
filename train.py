# This Python file uses the following encoding: utf-8
import argparse
import os
import re
import pickle

MAX_PREFIX_LENGTH = 10  # максимальное количество слов в префиксе


def generate_model(content, prefixes):
    tokens = list(map(lambda x: x.lower(), re.findall(r'[А-яЁё]+', content)))
    for i in range(len(tokens)):
        prefix = tokens[i]
        num = i
        while True:
            if num + 1 < len(tokens):
                if prefix in prefixes.keys():
                    prefixes[prefix].append(tokens[num + 1])
                    # print(prefix, prefixes[prefix])
                else:
                    prefixes[prefix] = [tokens[num + 1]]
                    # print(prefix, prefixes[prefix])
                prefix += ' ' + tokens[num + 1]
            num += 1
            if not (num < i + MAX_PREFIX_LENGTH < len(tokens)) or not tokens[num]:
                break

    return prefixes


parser = argparse.ArgumentParser(description='Скрипт обучения модели')
parser.add_argument(
    "--model",
    type=str,
    help="путь к файлу, в который сохраняется модель"
)
parser.add_argument(
    "--input-dir",
    type=str,
    help="путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты "
         "вводятся из stdin "
)
args = parser.parse_args()
if not args.model:
    parser.print_help()
    exit(0)

pattern = re.compile('[А-Яа-яЁё]+')

final_model = dict()
if args.input_dir:
    arr = next(os.walk(str(args.input_dir)))[2]
    for file in arr:
        print('Обрабатывается файл: ' + file)
        with open(os.path.join(str(args.input_dir), file), 'r', encoding="utf-8") as content_file:
            cont = content_file.read()
            final_model = generate_model(cont, final_model)
else:
    cont = input('Введите текст для обучения:\r\n')
    final_model = generate_model(cont, final_model)

with open(str(args.model), 'wb') as model_file:
    pickle.dump(final_model, model_file, protocol=pickle.HIGHEST_PROTOCOL)
