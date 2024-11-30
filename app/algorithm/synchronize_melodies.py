import logging
import app.algorithm.extract_notes as extract_notes

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def synchronize_melodies(teacher_melody, children_melody, min_per_t, min_per_c):
    """
    Синхронизирует мелодии учителя и ребенка, извлекая ноты и частоты.

    Эта функция принимает две мелодии (учительскую и детскую) и минимальные 
    параметры для извлечения нот. Она вызывает вспомогательную функцию 
    `extract_notes` для каждой мелодии, чтобы получить все ноты, частоты 
    и метки. В конце функция возвращает извлеченные данные для обеих мелодий.

    Параметры:
    teacher_melody (list): Список нот учительской мелодии.
    children_melody (list): Список нот детской мелодии.
    min_per_t (float): Минимальный параметр для извлечения нот учительской мелодии.
    min_per_c (float): Минимальный параметр для извлечения нот детской мелодии.

    Возвращает:
    tuple: Кортеж, содержащий:
        - all_t (list): Все ноты учительской мелодии.
        - all_c (list): Все ноты детской мелодии.
        - freq_t (list): Частоты учительской мелодии.
        - freq_c (list): Частоты детской мелодии.
        - t_m (list): Метки для учительской мелодии.
        - c_m (list): Метки для детской мелодии.

    Исключения:
    Exception: Если возникает ошибка при синхронизации мелодий, функция 
    записывает сообщение об ошибке в лог и возвращает (None, None, None, None, None, None).
    """
    logging.info("Начало синхронизации мелодий")
    try:
        all_t, freq_t, t_m = extract_notes(teacher_melody, min_per_t)
        all_c, freq_c, c_m = extract_notes(children_melody, min_per_c)
        logging.info("Синхронизация завершена")
        return all_t, all_c, freq_t, freq_c, t_m, c_m
    except Exception as e:
        logging.error("Ошибка в функции %s: %s", __name__, str(e))
        return None, None, None, None, None, None