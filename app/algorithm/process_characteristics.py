import logging

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(levelname)s - %(message)s') 

def process_characteristics(x, time):
    """
    Обрабатывает входные данные и извлекает бинарные характеристики на основе заданного времени.

    Эта функция принимает список значений и время, затем вычисляет среднее 
    значение для каждого интервала, определяемого временем. Если среднее 
    значение в интервале больше или равно 0.5, функция добавляет 1 в 
    результирующий список, иначе — 0. Функция возвращает список бинарных 
    характеристик, основанный на входных данных.

    Параметры:
    x (list): Список значений, которые необходимо обработать.
    time (float): Время в секундах, определяющее длину интервала для вычисления.

    Возвращает:
    list: Список бинарных характеристик, где 1 указывает на среднее значение 
    больше или равно 0.5, а 0 — меньше.

    Исключения:
    None: Если время равно нулю, функция возвращает пустой список и 
    записывает предупреждение в лог.
    """
    
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