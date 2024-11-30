import logging
import app.algorithm.extract_melody_from_audio as extract_melody_from_audio
import app.algorithm.synchronize_melodies as synchronize_melodies
import app.algorithm.compare_melody_sequences as compare_melody_sequences
import app.algorithm.compare as compare

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def compare_melodies(file1, file2):
    """
    Сравнивает мелодии из двух аудиофайлов и возвращает результаты анализа.

    Эта функция принимает два аудиофайла, извлекает из них мелодии 
    (учительскую и детскую), синхронизирует их и сравнивает характеристики. 
    Функция возвращает результаты сравнения, включая показатели громкости, 
    ритма и высоты звука.

    Параметры:
    file1 (str): Путь к аудиофайлу учителя.
    file2 (str): Путь к аудиофайлу ребенка.

    Возвращает:
    tuple: Результаты сравнения, содержащие интегральный индикатор схожести 
    и характеристики мелодий, или None, если произошла ошибка.

    Исключения:
    Exception: Если возникает ошибка при извлечении мелодий или их сравнении, 
    функция записывает сообщение об ошибке в лог и возвращает None.
    """

    logging.info("Начало сравнения мелодий")
    try:
        teacher_melody, min_per_t = extract_melody_from_audio(file1)
        if teacher_melody is None:
            logging.error("Не удалось получить мелодию учителя")
            return None

        children_melody, min_per_c = extract_melody_from_audio(file2)
        if children_melody is None:
            logging.error("Не удалось получить мелодию ребенка")
            return None

        all_t, all_c, freq_t, freq_c, t_m, c_m = synchronize_melodies(teacher_melody, children_melody, min_per_t, min_per_c)

        teacher_melody, children_melody, freq_t, freq_c, t_m, c_m = compare_melody_sequences(
            all_t, all_c, freq_t, freq_c, t_m, c_m, teacher_melody, children_melody
        )

        result = compare(t_m, c_m, freq_t, freq_c, teacher_melody, children_melody, 2)
        logging.info("Сравнение мелодий завершено")
        return result

    except Exception as e:
        logging.error("Ошибка в функции %s: %s", __name__, str(e))
        return None