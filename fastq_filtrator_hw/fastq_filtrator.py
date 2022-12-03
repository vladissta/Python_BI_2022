def making_dict(file):
    """
    Создание списка словарей с 4 элементами соответствующими строчкам одного прочтения.

    :param file: файл .fastq
    :return: список из словарей
    """
    full_list = []
    for line in file:
        full_list.append({
            'name': line.strip(),
            'seq': file.readline().strip(),
            'plus': file.readline().strip(),
            'quality': file.readline().strip()})
    return full_list


def filter_len(read, length_bounds):
    """
    Если дается две границы, то если прочтение длиной попадает в эти границы включительно, возвращает True.
    Если дается одна граница, то если прочтение длиной меньше этой границы, возвращает True.

    :param read: прочтение, у которого проверяем попадает ли его длина в установленные границы.
    :param length_bounds: границы фильтрации по длине (в нуклеотидах).
    :return: True/False
    """
    if isinstance(length_bounds, (list, tuple)):
        if length_bounds[0] <= len(read['seq']) <= length_bounds[1]:
            return True
    else:
        if len(read['seq']) <= length_bounds:
            return True


def filter_gc_percentage(read, gc_bounds):
    """
    Если дается две границы, то если прочтение по GC-составу попадает в эти границы включительно, возвращает True.
    Если дается одна граница, то если прочтение по GC-составу меньше этой границы, возвращает True.

    :param read: прочтение, у которого проверяем попадает ли его длина в установленные границы.
    :param gc_bounds: границы фильтрации по GC-составу (в процентах).
    :return: True/False
    """
    gc = 0
    for nucl in read['seq']:
        if nucl.upper() == 'G' or 'C':
            gc += 1
    prc = (gc / len(read['seq'])) * 100

    if isinstance(gc_bounds, (list, tuple)):
        if gc_bounds[0] <= prc <= gc_bounds[1]:
            return True
    else:
        if prc <= gc_bounds:
            return True
    return False


def filter_mean_quality(read, qual_threshold):
    """
    Дается одна граница, функция возвращает True, если прочтение по среднему качеству большие или равно границе.
    Качество считается в значениях шкалы phred33, переводя ascii-символы в их численные значения

    :param read: прочтение, у которого проверяем попадает ли его длина в установленные границы.
    :param qual_threshold: граница фильтрации по среднему качеству прочтений (в процентах)
    :return: True/False
    """
    qualities = [ord(i) - 33 for i in read['quality']]
    mean = sum(qualities) / len(qualities)
    if mean >= qual_threshold:
        return True
    return False


def file_writing(dicts, prefix, is_failed=False):
    """
    Создание файлов с прочтениями .
    Название {prefix}_passed.fastq или {prefix}_failed.fastq в зависимости от параметра is_failed

    :param is_failed: True/False в зависимости от того нужно нам записать в файл прочтения прошедшие фильтрацию или нет.
    :param dicts: список словарей с прочтениями.
    :param prefix: префикс в начале названия файла.
    :return: None
    """
    if is_failed:
        file_name = 'passed'
    else:
        file_name = 'failed'

    with open(f'{prefix}_{file_name}.fastq', 'w') as file:
        for read in dicts:
            for line in read.values():
                print(line, file=file)


def main(input_fastq, output_file_prefix, gc_bounds=(0, 100),
         length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=False):
    """
    Функция, в которой происходит вся фильтрация и запись файлов.

    :param input_fastq: файл fastq, который надо отфильтровать.
    :param output_file_prefix: префикс, с которым будут создаваться новые файлы
    с прошедшими и непрошедшими фильтрацию прочтениями.
    :param gc_bounds: границы фильтрации по GC-составу (в процентах).
    :param length_bounds: границы фильтрации по длине (в нуклеотидах).
    :param quality_threshold: нижняя граница фильтрации по среднему качеству прочтений (в процентах).
    :param save_filtered: параметр, указывающий нужно ли сохранять отдельным файлом прочтения не прошедшие фильтрацию.
    :return: None
    """

    with open(input_fastq) as file:
        full_dicts = making_dict(file)  # список словарей с 4 элементами соответствующим строчкам одного прочтения

        # filtering
        failed = []
        for n, read in enumerate(full_dicts):
            fil_len = filter_len(read, length_bounds)
            fil_gc = filter_gc_percentage(read, gc_bounds)
            fil_qual = filter_mean_quality(read, quality_threshold)

            if fil_len and fil_gc and fil_qual:
                failed.append(full_dicts.pop(n))

        # запись файлов
        file_writing(full_dicts, output_file_prefix)

        if save_filtered:
            file_writing(failed, output_file_prefix, is_failed=True)
