import librosa.feature
import numpy as np
from math import floor

# Первый модуль
# Приведение мелодии к виду, пригодному для обработки
def start_coparing(file_path):
    # Загрузка аудиозаписи и образание шумов в начале и конце мелодии
    tm, srt = librosa.load(file_path)
    tmt, _ = librosa.effects.trim(tm, top_db=14)

    # Расчет мел-спектрограммы, вывод матрицы значений
    tmt_mel = librosa.feature.melspectrogram(y=tmt, sr=srt, n_mels=64)
    tmt_db_mel = librosa.amplitude_to_db(tmt_mel)[4:9]

    # Подготовка матрицы к обработке
    tmt_db_mel_transponsed = np.transpose(tmt_db_mel)

    # Расчет длительности мелодии
    time_t = librosa.get_duration(S=tmt_mel, sr=srt)
    min_per_t = round(len(tmt_db_mel_transponsed))/(time_t*4)

    # Цикл возвращает списоком последовательность значений всей аудиозаписи;
    teacher_melody = []

    for i in tmt_db_mel_transponsed:
        counter = 0
        if all(map(lambda y: y < 0, i)):
            counter += 1
        else:
            max_index = [y for y, val in enumerate(i) if val == max(i)]
            teacher_melody.append(int(max_index[0]) + ((round(max(i))) / 100))
            if counter < min_per_t:
                while counter != 0:
                    teacher_melody.append(float(max_index[0]))
                    counter -= 1
            else:
                while counter != 0:
                    teacher_melody.append(float(0))
                    counter -= 1

    return teacher_melody, min_per_t

# Второй модуль
# Синхронизации мелодий и устранение временной разнесенности нот
def sync(teacher_melody, children_melody, min_per_t, min_per_c):
    counter_t = 0
    counter_c = 0
    all_t = []
    all_c = []
    freq_t = []
    freq_c = []
    t_m = []
    c_m = []

    for i in range(0, len(teacher_melody)-1):
        if floor(teacher_melody[i]) == floor(teacher_melody[i+1]):
            counter_t += 1
        elif floor(teacher_melody[i]) != floor(teacher_melody[i+1]) and counter_t >= min_per_t:
            all_t.append(floor(teacher_melody[i]) + counter_t/100)
            freq_t.append(floor(teacher_melody[i]))
            t_m.append(counter_t)
            counter_t = 0
        else:
            counter_t = 0

    for i in range(0, len(children_melody)-1):
        if floor(children_melody[i]) == floor(children_melody[i+1]):
            counter_c += 1
        elif floor(children_melody[i]) != floor(children_melody[i+1]) and counter_c >= min_per_c:
            all_c.append(floor(children_melody[i]) + counter_c/100)
            freq_c.append(floor(children_melody[i]))
            c_m.append(counter_c)
            counter_c = 0
        else:
            counter_c = 0

    return all_t, all_c, freq_t, freq_c, t_m, c_m

def check_notes(all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody):
    exec_t = []
    exec_c = []
    
    if len(all_t) != len(all_c) and len(all_t) < len(all_c):
        for i in range(0, len(all_t)-3):
            if all_c[i] != all_t[i] and all_c[i+1: i+3] == all_t[i: i+2]:
                exec_c.append(i + all_c % 1)
            elif all_c[i] != all_t[i] and all_c[i: i+2] == all_t[i+1: i+3]:
                exec_t.append(i + all_t % 1)
    elif len(all_t) != len(all_c) and len(all_t) > len(all_c):
        for i in range(0, len(all_c)-4):
            if all_c[i] != all_t[i] and all_c[i+1: i+3] == all_t[i: i+2]:
                exec_c.append(i + all_c % 1)
            elif all_c[i] != all_t[i] and all_c[i: i+2] == all_t[i+1: i+3]:
                exec_t.append(i + all_t % 1)

    while len(exec_c) != 0:
        t_m.insert(floor(exec_c[0]), 1)
        freq_t.insert(floor(exec_c[0]), 6)
        exec_c = exec_c[1:]
        exec_c = list(map(lambda y: y + 1, exec_c))

    while len(exec_t) != 0:
        c_m.insert(floor(exec_t[0]), 1)
        freq_c.insert(floor(exec_t[0]), 6)
        exec_t = exec_t[1:]
        exec_t = list(map(lambda y: y + 1, exec_t))

    # Выравнивание характеристик по длине
    while len(teacher_melody) != len(children_melody):
        if len(teacher_melody) > len(children_melody):
            children_melody.append(float(0))
        elif len(teacher_melody) < len(children_melody):
            teacher_melody.append(float(0))

    while len(freq_c) != len(freq_t):
        if len(freq_t) > len(freq_c):
            freq_c.append(0)
        elif len(freq_t) < len(freq_c):
            freq_t.append(0)

    while len(t_m) != len(c_m):
        if len(t_m) > len(c_m):
            c_m.append(1)
        elif len(t_m) < len(c_m):
            t_m.append(1)

    return teacher_melody, children_melody, freq_t, freq_c, t_m, c_m

def compare(t_m, c_m, freq_t, freq_c):
    # Сравнение ритма
    res_rhythm = []
    for i in range(0, len(t_m)):
        if abs((t_m[i] - c_m[i]) / t_m[i]) <= 0.25:
            res_rhythm += [0] * c_m[i]
        elif t_m[i] < c_m[i]:
            res_rhythm += [0] * t_m[i] + [1] * abs(c_m[i] - t_m[i])
        elif t_m[i] > c_m[i]:
            res_rhythm += [0] * c_m[i] + [1] * abs(t_m[i] - c_m[i])

    # Сравнение частот
    res_frequency = []
    for i in range(0, len(freq_t)):
        if freq_t[i] == freq_c[i]:
            res_frequency += [0] * c_m[i]
        else:
            res_frequency += [1] * c_m[i]

    # Результаты сравнений, приведенные по времени
    integral_indicator = 1 - round(sum(res_rhythm + res_frequency) / len(res_rhythm + res_frequency), 2)

    return integral_indicator


def compare_melodies(file_path1, file_path2):
    teacher_melody, min_per_t = start_coparing(file_path1)
    children_melody, min_per_c = start_coparing(file_path2)

    all_t, all_c, freq_t, freq_c, t_m, c_m = sync(teacher_melody, children_melody, min_per_t, min_per_c)

    teacher_melody, children_melody, freq_t, freq_c, t_m, c_m = check_notes(all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody)

    index = compare(t_m, c_m, freq_t, freq_c)

    return index