import logging
from math import floor

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def extract_notes(melody, min_per):
    """
    Извлекает ноты из мелодии, основываясь на минимальной продолжительности повторений.

    Эта функция принимает список нот (мелодию) и минимальный параметр 
    для определения, сколько раз нота должна повторяться, чтобы быть 
    извлеченной. Функция проходит по мелодии и накапливает повторяющиеся 
    ноты, добавляя их в список, если количество повторений превышает 
    заданный минимум. Возвращаются извлеченные ноты, их частоты и длины.

    Параметры:
    melody (list): Список нот, из которого необходимо извлечь повторяющиеся ноты.
    min_per (int): Минимальное количество повторений, необходимое для извлечения ноты.

    Возвращает:
    tuple: Кортеж, содержащий:
        - all_notes (list): Список извлеченных нот.
        - freq (list): Список частот извлеченных нот.
        - lengths (list): Список длин повторений для каждой извлеченной ноты.

    Исключения:
    Exception: Если возникает ошибка при извлечении нот, функция 
    записывает сообщение об ошибке в лог и возвращает пустые списки.
    """
    
    logging.info("Начало извлечения нот")
    counter = 0
    all_notes = []
    freq = []
    lengths = []

    try:
        for i in range(len(melody) - 1):
            if floor(melody[i]) == floor(melody[i + 1]):
                counter += 1
            elif counter >= min_per:
                all_notes.append(floor(melody[i]) + counter / 100)
                freq.append(floor(melody[i]))
                lengths.append(counter)
                counter = 0

        logging.info("Извлечение нот завершено, найдено %d нот", len(all_notes))
        return all_notes, freq, lengths

    except Exception as e:
        logging.error("Ошибка в функции %s: %s", __name__, str(e))
        return [], [], []