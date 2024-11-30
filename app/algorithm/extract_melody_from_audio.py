import librosa
import librosa.feature
import numpy as np
import logging

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def extract_melody_from_audio(file_bytes):
    """
    Сравнивает аудиофайл, извлекая мелодию и вычисляя минимальную продолжительность.

    Эта функция загружает аудиофайл из байтового потока, обрезает его по тишине,
    вычисляет мелоспектрограмму и извлекает ноты, представляя их в виде индексов
    и значений громкости. Функция возвращает список извлеченных нот и минимальную
    продолжительность в виде значения.

    Параметры:
    file_bytes (bytes): Байтовый поток аудиофайла, который необходимо обработать.

    Возвращает:
    tuple: Кортеж, содержащий:
        - list: Список извлеченных нот (индексы и значения громкости).
        - float: Минимальная продолжительность в виде значения.

    Исключения:
    Exception: Если возникает ошибка при загрузке или обработке аудиофайла,
    функция записывает сообщение об ошибке в лог и возвращает (None, None).
    """
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
        logging.error("Ошибка в функции %s: %s", __name__, str(e))
        return None, None