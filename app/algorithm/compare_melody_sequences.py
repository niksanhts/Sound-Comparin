from math import floor
import logging

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def compare_melody_sequences(all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody):
    """
    Проверяет и сравнивает ноты между учительской и детской мелодиями, 
    а также обновляет частоты и метки для каждой из мелодий.

    Эта функция принимает две последовательности нот (учительскую и детскую) 
    и проверяет их на совпадения. Если обнаруживаются расхождения, 
    функция обновляет соответствующие метки и частоты. В конце функция 
    выравнивает длины всех выходных списков, добавляя нули и единицы, 
    чтобы они имели одинаковую длину.

    Параметры:
    all_t (list): Список нот учителя.
    all_c (list): Список нот ребенка.
    freq_t (list): Список частот учительской мелодии.
    freq_c (list): Список частот детской мелодии.
    t_m (list): Метки для учительской мелодии.
    c_m (list): Метки для детской мелодии.
    teacher_melody (list): Список учительской мелодии.
    children_melody (list): Список детской мелодии.

    Возвращает:
    tuple: Кортеж, содержащий обновленные списки:
        - teacher_melody (list): Обновленный список учительской мелодии.
        - children_melody (list): Обновленный список детской мелодии.
        - freq_t (list): Обновленный список частот учительской мелодии.
        - freq_c (list): Обновленный список частот детской мелодии.
        - t_m (list): Обновленный список меток для учительской мелодии.
        - c_m (list): Обновленный список меток для детской мелодии.

    Исключения:
    Exception: Если возникает ошибка при проверке нот, функция записывает 
    сообщение об ошибке в лог и возвращает исходные списки.
    """

    logging.info("Начало проверки нот")
    exec_t = []
    exec_c = []

    try:
        if len(all_t) != len(all_c):
            for i in range(min(len(all_t), len(all_c)) - 3):
                if all_c[i] != all_t[i] and all_c[i + 1:i + 3] == all_t[i:i + 2]:
                    exec_c.append(i + all_c[i] % 1)
                elif all_c[i] != all_t[i] and all_c[i:i + 2] == all_t[i + 1:i + 3]:
                    exec_t.append(i + all_t[i] % 1)

        for idx in exec_c:
            idx = floor(idx)
            t_m.insert(idx, 1)
            freq_t.insert(idx, 6)

        for idx in exec_t:
            idx = floor(idx)
            c_m.insert(idx, 1)
            freq_c.insert(idx, 6)

        max_length = max(len(teacher_melody), len(children_melody))
        teacher_melody.extend([0.0] * (max_length - len(teacher_melody)))
        children_melody.extend([0.0] * (max_length - len(children_melody)))

        max_length = max(len(freq_t), len(freq_c))
        freq_t.extend([0] * (max_length - len(freq_t)))
        freq_c.extend([0] * (max_length - len(freq_c)))

        max_length = max(len(t_m), len(c_m))
        t_m.extend([1] * (max_length - len(t_m)))
        c_m.extend([1] * (max_length - len(c_m)))

        logging.info("Проверка нот завершена")
        return teacher_melody, children_melody, freq_t, freq_c, t_m, c_m

    except Exception as e:
        logging.error("Ошибка в функции check_notes: %s", str(e))
        return teacher_melody, children_melody, freq_t, freq_c, t_m, c_m