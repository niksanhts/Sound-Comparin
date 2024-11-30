import app.algorithm.process_characteristics as process_characteristics
import logging

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody, time_c):
    """
    Сравнивает характеристики мелодий учителя и ребенка, вычисляя различные показатели.

    Эта функция принимает метки, частоты и мелодии учителя и ребенка, 
    а также время для анализа. Она сравнивает громкость, ритм, высоту 
    звука и частоты, возвращая интегральный индикатор схожести и 
    характеристики для каждой из категорий. Функция также обрабатывает 
    характеристики громкости и высоты звука.

    Параметры:
    t_m (list): Метки для учительской мелодии.
    c_m (list): Метки для детской мелодии.
    freq_t (list): Частоты учительской мелодии.
    freq_c (list): Частоты детской мелодии.
    teacher_melody (list): Список учительской мелодии.
    children_melody (list): Список детской мелодии.
    time_c (float): Время для обработки характеристик.

    Возвращает:
    tuple: Кортеж, содержащий:
        - integral_indicator (float): Интегральный индикатор схожести мелодий.
        - rhythm (list): Обработанные характеристики ритма.
        - height (list): Обработанные характеристики высоты звука.
        - volume1 (list): Обработанные характеристики громкости.
        - volume2 (list): Нормализованные значения громкости детской мелодии.

    Исключения:
    None: Функция не обрабатывает исключения, но записывает сообщения в лог 
    о начале и завершении сравнения.
    """
    logging.info("Начало сравнения мелодий")
    res_loud = []
    teacher_melody = [round((y % 1) * 100) for y in teacher_melody]
    children_melody = [round((y % 1) * 100) for y in children_melody]

    counter_t = 0
    counter_c = 0
    for i in range(len(t_m)):
        t_sum = sum(teacher_melody[counter_t:counter_t + t_m[i]])
        c_sum = sum(children_melody[counter_c:counter_c + c_m[i]])
        if t_sum != 0 and abs(1 - (c_sum / c_m[i]) / (t_sum / t_m[i])) <= 0.25:
            res_loud.extend([0] * c_m[i])
        else:
            res_loud.extend([1] * c_m[i])
        counter_t += t_m[i]
        counter_c += c_m[i]

    res_rhythm = []
    for i in range(len(t_m)):
        if abs((t_m[i] - c_m[i]) / t_m[i]) <= 0.25:
            res_rhythm += [0] * c_m[i]
        else:
            diff = abs(c_m[i] - t_m[i])
            res_rhythm += [0] * min(t_m[i], c_m[i]) + [1] * diff

    res_average = []
    max_c = max(children_melody) if children_melody else 1
    for i in range(len(children_melody)):
        res_average.append(round(children_melody[i] / max_c, 2))

    res_frequency = []
    for i in range(len(freq_t)):
        if freq_t[i] == freq_c[i]:
            res_frequency += [0] * c_m[i]
        else:
            res_frequency += [1] * c_m[i]

    total_errors = res_rhythm + res_frequency
    integral_indicator = 1 - round(sum(total_errors) / len(total_errors), 2)
    rhythm = process_characteristics(res_rhythm, time_c)
    height = process_characteristics(res_frequency, time_c)
    volume1 = process_characteristics(res_loud, time_c)
    volume2 = res_average

    logging.info("Сравнение мелодий завершено")
    return integral_indicator, rhythm, height, volume1, volume2