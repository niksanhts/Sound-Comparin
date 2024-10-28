import librosa
import librosa.feature
import numpy as np
from math import floor

# Первый модуль
# Приведение мелодии к виду, пригодному для обработки
def start_comparing(file_bytes):
    # Загрузка аудиозаписи из байтового потока и обрезка шумов в начале и конце мелодии
    tm, srt = librosa.load(file_bytes, sr=None)  # Загрузка без изменения частоты
    tmt, _ = librosa.effects.trim(tm, top_db=14)

    # Расчет мел-спектрограммы, вывод матрицы значений
    tmt_mel = librosa.feature.melspectrogram(y=tmt, sr=srt, n_mels=64)
    tmt_db_mel = librosa.amplitude_to_db(tmt_mel)[4:9]

    # Подготовка матрицы к обработке
    tmt_db_mel_transposed = np.transpose(tmt_db_mel)

    # Расчет длительности мелодии
    time_t = librosa.get_duration(S=tmt_mel, sr=srt)
    min_per_t = round(len(tmt_db_mel_transposed)) / (time_t * 4)

    # Цикл возвращает последовательность значений всей аудиозаписи
    teacher_melody = []
    counter = 0

    for i in tmt_db_mel_transposed:
        if all(map(lambda y: y < 0, i)):
            counter += 1
        else:
            max_index = [y for y, val in enumerate(i) if val == max(i)]
            teacher_melody.append(int(max_index[0]) + ((round(max(i))) / 100))
            while counter > 0:
                teacher_melody.append(float(0))
                counter -= 1

    return teacher_melody, min_per_t

# Второй модуль
# Синхронизация мелодий и устранение временной разнесенности нот
def sync(teacher_melody, children_melody, min_per_t, min_per_c):
    counter_t = 0
    counter_c = 0
    all_t = []
    all_c = []
    freq_t = []
    freq_c = []
    t_m = []
    c_m = []

    for i in range(len(teacher_melody) - 1):
        if floor(teacher_melody[i]) == floor(teacher_melody[i + 1]):
            counter_t += 1
        elif counter_t >= min_per_t:
            all_t.append(floor(teacher_melody[i]) + counter_t / 100)
            freq_t.append(floor(teacher_melody[i]))
            t_m.append(counter_t)
            counter_t = 0

    for i in range(len(children_melody) - 1):
        if floor(children_melody[i]) == floor(children_melody[i + 1]):
            counter_c += 1
        elif counter_c >= min_per_c:
            all_c.append(floor(children_melody[i]) + counter_c / 100)
            freq_c.append(floor(children_melody[i]))
            c_m.append(counter_c)
            counter_c = 0

    return all_t, all_c, freq_t, freq_c, t_m, c_m

# Третий модуль
# Проверка нот и приведение их к одной длине
def check_notes(all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody):
    exec_t = []
    exec_c = []

    if len(all_t) != len(all_c):
        for i in range(min(len(all_t), len(all_c)) - 3):
            if all_c[i] != all_t[i] and all_c[i + 1:i + 3] == all_t[i:i + 2]:
                exec_c.append(i + all_c[i] % 1)
            elif all_c[i] != all_t[i] and all_c[i:i + 2] == all_t[i + 1:i + 3]:
                exec_t.append(i + all_t[i] % 1)

    while exec_c:
        idx = floor(exec_c[0])
        t_m.insert(idx, 1)
        freq_t.insert(idx, 6)
        exec_c = list(map(lambda y: y + 1, exec_c[1:]))

    while exec_t:
        idx = floor(exec_t[0])
        c_m.insert(idx, 1)
        freq_c.insert(idx, 6)
        exec_t = list(map(lambda y: y + 1, exec_t[1:]))

    max_length = max(len(teacher_melody), len(children_melody))
    teacher_melody.extend([0.0] * (max_length - len(teacher_melody)))
    children_melody.extend([0.0] * (max_length - len(children_melody)))

    max_length = max(len(freq_t), len(freq_c))
    freq_t.extend([0] * (max_length - len(freq_t)))
    freq_c.extend([0] * (max_length - len(freq_c)))

    max_length = max(len(t_m), len(c_m))
    t_m.extend([1] * (max_length - len(t_m)))
    c_m.extend([1] * (max_length - len(c_m)))

    return teacher_melody, children_melody, freq_t, freq_c, t_m, c_m

# Четвертый модуль
# Сравнение мелодий
def compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody):
    # Сравнение громкости
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

    # Сравнение ритма
    res_rhythm = []
    for i in range(len(t_m)):
        if abs((t_m[i] - c_m[i]) / t_m[i]) <= 0.25:
            res_rhythm += [0] * c_m[i]
        else:
            diff = abs(c_m[i] - t_m[i])
            res_rhythm += [0] * min(t_m[i], c_m[i]) + [1] * diff

    # Сравнение частот
    res_frequency = []
    for i in range(len(freq_t)):
        if freq_t[i] == freq_c[i]:
            res_frequency += [0] * c_m[i]
        else:
            res_frequency += [1] * c_m[i]

    # Итоговый интегральный показатель
    total_errors = res_rhythm + res_frequency
    integral_indicator = 1 - round(sum(total_errors) / len(total_errors), 2)

    return integral_indicator

# Финальная функция
def compare_melodies(file_path1, file_path2):
    teacher_melody, min_per_t = start_comparing(file_path1)
    children_melody, min_per_c = start_comparing(file_path2)

    all_t, all_c, freq_t, freq_c, t_m, c_m = sync(teacher_melody, children_melody, min_per_t, min_per_c)

    teacher_melody, children_melody, freq_t, freq_c, t_m, c_m = check_notes(
        all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody
    )

    index = compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody)

    return index
