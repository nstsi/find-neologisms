import re
import pandas as pd

import nltk

nltk.download('punkt')

DATA_FOLDER = 'data/'
# FILE_TO_PROCESS = input()
FILE_TO_PROCESS = 'DAr_8_1.txt'
FILE_TO_PROCESS_PATH = f'{DATA_FOLDER}{FILE_TO_PROCESS}'
FILE_TO_PROCESS_NAME = FILE_TO_PROCESS[:-4]
RESULTS_FILE = f'{FILE_TO_PROCESS_NAME}_results.txt'


def read_text(filename: str) -> str:
    with open(filename, encoding='utf-8') as txt:
        text_ = txt.read()
    return text_


def make_one_line(text_: str) -> str:
    text_ = re.sub('\n', ' ', text_)
    return text_


def split_in_sentences(text_: str) -> list:
    sentences_ = nltk.tokenize.sent_tokenize(text_)
    return sentences_


def make_neologisms_df():
    neologisms_ = pd.read_csv('data/neologisms_table.csv', delimiter=',')
    return neologisms_


def find_neologisms(text_one_line_: str,
                    sentences_: list,
                    neologisms_):
    """Описание ф-и"""
    column_names = neologisms_.columns.tolist()
    columns_add = ['current_sentence', 'previous_sentence', 'next_sentence']
    for elem in columns_add:
        column_names.append(elem)

    results = pd.DataFrame(columns=column_names)
    for index, row in neologisms_.iterrows():
        if row['word'] in text_one_line_:
            for i, sentence in enumerate(sentences_):
                if row['word'] in sentence:
                    current_sentence = sentence

                    try:
                        previous_sentence = sentences_[i-1]

                    except IndexError:
                        previous_sentence = 'пусто'

                    try:
                        next_sentence = sentences_[i+1]
                    except IndexError:
                        next_sentence = 'пусто'
                    res_list = [row['word'],
                                row['meaning'],
                                row['linguistic process'],
                                row['mistake location'],
                                row['mistake type'],
                                row['L1 interference'],
                                row['source'],
                                row['enTenTen18'],
                                current_sentence,
                                previous_sentence,
                                next_sentence]
                    df_length = len(results)
                    results.loc[df_length] = res_list
                    break  # берём только первое вхождение
    return results


def save_to_file(results, results_filename, text_filename):

    if results.empty:
        print(f'В тексте {text_filename} не были найдены новообразования.')
    else:
        with open(results_filename, 'w', encoding='utf-8') as f:

            f.write(f'В тексте {text_filename} были найдены следующие '
                    f'новообразования:')
            f.write('\n')

            for i in range(results.shape[0]):

                f.write(f'{i+1}.')
                f.write('\n')

                print(results.iloc[i])
                word = results.iloc[i]['word']
                meaning = results.iloc[i]['meaning']
                ling_proc = results.iloc[i]['linguistic process']
                mistake_loc = results.iloc[i]['mistake location']
                print(mistake_loc)
                mistake_type = results.iloc[i]['mistake type']
                print(mistake_type)
                l1_interference = results.iloc[i]['L1 interference']
                en18 = results.iloc[i]['enTenTen18']

                f.write(f'• Новообразование: {word} | '
                        f'Значение: {meaning} | '
                        f'Лингвистический процесс: {ling_proc} | '
                        f'Локация ошибки: {mistake_loc} | '
                        f'Тип ошибки: {mistake_type} | '
                        f'Возможность L1 interference: {l1_interference} | '
                        f'Количество вхождений в enTenTen18: {en18}')
                f.write('\n')

                curr_sent = results.iloc[i]['current_sentence']
                f.write(f'• Предложение: {curr_sent}')
                f.write('\n')

                prev_sent = results.iloc[i]['previous_sentence']
                next_sent = results.iloc[i]['next_sentence']
                context = f'{prev_sent} {curr_sent} {next_sent}'
                clean_context = re.sub(' пусто', '', context)

                f.write(f'• Контекст: {clean_context}')
                f.write('\n')

                source = results.iloc[i]['source']
                f.write(f'• Другие тексты с этим новообразованием: {source}')
                f.write('\n')

                if results.iloc[i][0] == results.iloc[-1][0]:
                    print(f'Найденные новообразования записаны в файл '
                          f'{results_filename}.')


def main():
    text = read_text(FILE_TO_PROCESS_PATH)
    text_one_line = make_one_line(text)
    sentences = split_in_sentences(text_one_line)
    neologisms = make_neologisms_df()
    results_df = find_neologisms(text_one_line, sentences, neologisms)
    save_to_file(results_df, RESULTS_FILE, FILE_TO_PROCESS_NAME)


if __name__ == '__main__':
    main()
