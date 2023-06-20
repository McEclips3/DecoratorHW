import datetime
from functools import wraps


import os


def debug_decor(origin_function):
    freddy = {}

    @wraps(origin_function)
    def new_function(*args, **kwargs):
        name = origin_function.__name__
        start = datetime.datetime.now()
        time = str(start)
        result = origin_function(*args, **kwargs)
        freddy['Name'] = name
        freddy['args'] = args, kwargs
        freddy['time'] = time
        freddy['result'] = result
        log_str = str(freddy)
        print(log_str)
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write('\n' + log_str)
        return result

    new_function.origin = origin_function

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @debug_decor
    def hello_world():
        return 'Hello World'

    @debug_decor
    def summator(a, b=0):
        return a + b

    @debug_decor
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()