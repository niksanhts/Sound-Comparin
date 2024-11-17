import librosa
import librosa.feature
import numpy as np
from math import floor
import logging


logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def start_comparing(file_bytes):
    logging.info("Начало сравнения аудиофайла")
    try:
        tm, srt = librosa.load(file_bytes, sr=None)
        logging.info("Аудиофайл загружен успешно")
        
        tmt, _ = librosa.effects.trim(tm, top_db=14)
        logging.info("Аудиофайл обрезан по тишине")
        
        tmt_mel = librosa.feature.melspectrogram(y=tmt, sr=srt, n_mels=64)
        logging.info("Мелоспектрограмма вычислена")
        
        tmt_db_mel = librosa.amplitude_to_db(tmt_mel)[4:9]
        tmt_db_mel_transposed = np.transpose(tmt_db_mel)
        time_t = librosa.get_duration(y=tmt, sr=srt)
        min_per_t = round(len(tmt_db_mel_transposed)) / (time_t * 4)
        
        teacher_melody = []
        counter = 0

        for i in tmt_db_mel_transposed:
            if all(val < 0 for val in i):
                counter += 1
            else:
                max_index = np.argmax(i)
                teacher_melody.append(max_index + (round(max(i)) / 100))
                teacher_melody.extend([0.0] * counter)
                counter = 0

        logging.info("Сравнение аудиофайла завершено, найдено %d нот", len(teacher_melody))
        return teacher_melody, min_per_t

    except Exception as e:
        logging.error("Ошибка в функции start_comparing: %s", str(e))
        return None, None

def sync(teacher_melody, children_melody, min_per_t, min_per_c):
    logging.info("Начало синхронизации мелодий")
    try:
        all_t, freq_t, t_m = extract_notes(teacher_melody, min_per_t)
        all_c, freq_c, c_m = extract_notes(children_melody, min_per_c)
        logging.info("Синхронизация завершена")
        return all_t, all_c, freq_t, freq_c, t_m, c_m
    except Exception as e:
        logging.error("Ошибка в функции sync: %s", str(e))
        return None, None, None, None, None, None

def extract_notes(melody, min_per):
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
        logging.error("Ошибка в функции extract_notes: %s", str(e))
        return [], [], []

def check_notes(all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody):
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


def compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody, time_c):
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
    rhythm = res_character(res_rhythm, time_c)
    height = res_character(res_frequency, time_c)
    volume1 = res_character(res_loud, time_c)
    volume2 = res_average

    logging.info("Сравнение мелодий завершено")
    return integral_indicator, rhythm, height, volume1, volume2


def res_character(x, time):
    logging.info("Начало обработки характеристик")
    y = []
    time = round(time, 2)
    count_of_values = round(time * 4)

    if count_of_values == 0:
        logging.warning("Время равно нулю, возвращаем пустой список")
        return y

    while len(x) >= count_of_values:
        c = sum(x[:count_of_values]) / count_of_values
        y.append(1 if c >= 0.5 else 0)
        x = x[count_of_values:]

    if len(x) > 0:
        c = sum(x) / len(x)
        y.append(1 if c >= 0.5 else 0)

    logging.info("Обработка характеристик завершена, найдено %d значений", len(y))
    return y


def compare_melodies(file1, file2):
    logging.info("Начало сравнения мелодий")
    try:
        teacher_melody, min_per_t = start_comparing(file1)
        if teacher_melody is None:
            logging.error("Не удалось получить мелодию учителя")
            return None

        children_melody, min_per_c = start_comparing(file2)
        if children_melody is None:
            logging.error("Не удалось получить мелодию ребенка")
            return None

        all_t, all_c, freq_t, freq_c, t_m, c_m = sync(teacher_melody, children_melody, min_per_t, min_per_c)

        teacher_melody, children_melody, freq_t, freq_c, t_m, c_m = check_notes(
            all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody
        )

        result = compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody, 2)
        logging.info("Сравнение мелодий завершено")
        return result

    except Exception as e:
        logging.error("Ошибка в функции compare_melodies: %s", str(e))
        return None

