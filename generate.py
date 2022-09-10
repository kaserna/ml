import argparse
import pickle
import sys

import numpy as np

MAX_PREFIX_LENGTH = 2  # максимальное количество слов в префиксе

parser = argparse.ArgumentParser(description='Скрипт генерации текста')
parser.add_argument(
    "--model",
    type=str,
    help="путь к файлу, из которого загружается модель"
)
parser.add_argument(
    "--prefix",
    type=str,
    help="необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное "
         "слово случайно из всех слов "
)
parser.add_argument(
    "--length",
    type=int,
    help="длина генерируемой последовательности"
)

np.random.seed()

args = parser.parse_args()
if not args.model or not args.length:
    parser.print_help()
    exit(0)

print("Загрузка модели...")

with open(str(args.model), 'rb') as model_file:
    model = pickle.load(model_file)

print("Генерация...")

prefix = ''
if args.prefix:
    prefix = str(args.prefix)
else:
    prefix = np.random.choice(list(model.keys()))

phrase = prefix
for i in range(args.length):
    options = []
    prefix = ' '.join(phrase.split(' ')[-MAX_PREFIX_LENGTH:])
    if prefix in model.keys():
        options = model[prefix]
    if len(options) > 0:
        phrase += ' ' + np.random.choice(list(options))
    else:  # если нет вариантов, то пробуем сократить число слов в префиксе
        words = prefix.split(' ')
        cnt = len(words)
        while len(options) == 0 and cnt > 0:
            cnt -= 1
            newPrefix = ' '.join(phrase.split(' ')[cnt:])
            if newPrefix in model.keys():
                options = model[newPrefix]
        if cnt == 0:
            # раз нет вариантов, то выбираем случайное слово
            phrase += ' ' + np.random.choice(list(model.keys()))
        else:
            phrase += ' ' + np.random.choice(list(options))


print(phrase)

