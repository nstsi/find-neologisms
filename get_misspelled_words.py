import re
import csv

from spellchecker import SpellChecker
from os import listdir
from os.path import isfile, join

spell = SpellChecker()

FOLDER = input(f'Положите все файлы в формате .txt в новую папку внутри папки '
               f'data и введите имя этой новой папки: ')
FOLDER_PATH = f'data/{FOLDER}/'
RESULTS_FILE = f'{FOLDER}_results.csv'


def get_filenames(folder_path_: str) -> list:
    filenames_ = [f for f in listdir(folder_path_)
                  if isfile(join(folder_path_, f))]
    return filenames_


def read_text(filename_: str) -> str:
    with open(filename_, encoding='utf-8') as txt:
        text_ = txt.read()
    return text_


def make_one_line(text_: str) -> str:
    text_ = re.sub('\n', ' ', text_)
    return text_


def spit_text(text_: str, filename) -> list:
    text_letters = re.sub(r'[^a-zA-Z- /]', '', text_)
    clean_text = re.sub(r' - ', ' ', text_letters)
    words = clean_text.split()
    dict_words = [filename, words]
    return dict_words


def get_misspelled_words(dict_words):
    misspelled = spell.unknown(dict_words[1])
    mistakes = []
    for word in misspelled:
        mistakes.append(word)
    dict_mistakes = [[dict_words[0][:-4]], mistakes]
    if dict_mistakes[1]:
        row = [item for sublist in dict_mistakes for item in sublist]
        f = open(RESULTS_FILE, 'a')
        writer = csv.writer(f, delimiter='|')
        writer.writerow(row)
        f.close()


def main():
    filenames = get_filenames(FOLDER_PATH)
    for i in range(len(filenames)):
        file_path = f'{FOLDER_PATH}{filenames[i]}'
        text1 = read_text(file_path)
        text2 = make_one_line(text1)
        dict_words = spit_text(text2, filenames[i])
        get_misspelled_words(dict_words)
    print('Слова с ошибками записаны в файл .csv')


if __name__ == '__main__':
    main()
