def making_dict(file):
    """
    Создание списка словарей с 4 элементами соответсвуюшим строчкам одного прочтения

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


def filter_len(dicts, length_bounds):
    """
    Создание списка словарей прочтений прошедших фильтрацию по длине прочтений.
    Если дается две границы, выбираются прочтения длиной попадающие в эти границы включительно
    Если дается одна граница, выбираются прочтения по длине меньшие и равные границе

    :param dicts: список словарей полученный из функции full_dicts
    :param length_bounds: границы фильтрации по длине (в нуклеотидах)
    :return: список словарей прошедший фильтрацию по длине прочтений
    """
    filtered = []
    if isinstance(length_bounds, (list, tuple)):
        for d in dicts:
            if length_bounds[0] <= len(d['seq']) <= length_bounds[1]:
                filtered.append(d)
    else:
        for d in dicts:
            if len(d['seq']) <= length_bounds:
                filtered.append(d)

    return filtered


def filter_gc_percentage(dicts, gc_bounds):
    """
    Создание списка словарей прочтений прошедших фильтрацию по GC-составу.
    Если дается две границы, выбираются прочтения по GC-составу попадающие в эти границы включительно
    Если дается одна граница, выбираются прочтения по GC-составу меньшие и равные границе

    :param dicts: список словарей полученный из функции filter_len
    :param gc_bounds: границы фильтрации по GC-составу (в процентах)
    :return: список словарей прошедший фильтрацию по GC-составу
    """
    filtered = []

    for d in dicts:
        gc = 0
        for nucl in d['seq']:
            if nucl.upper() == 'G' or 'C':
                gc += 1
        prc = (gc / len(d['seq'])) * 100
        if isinstance(gc_bounds, (list, tuple)):
            if gc_bounds[0] <= prc <= gc_bounds[1]:
                filtered.append(d)
        else:
            if prc <= gc_bounds:
                filtered.append(d)
    return filtered


def filter_mean_quality(dicts, qual_threshold):
    """
    Создание списка словарей прочтений прошедших фильтрацию по среднему качеству прочтений.
    Дается одна граница, выбираются прочтения по среднему качеству большие и равные границе.
    Качество считается в значениях шкалы phred33, переводя ascii-символы в их численные значения

    :param dicts: список словарей полученный из функции filter_gc_percentage
    :param qual_threshold: граница фильтрации по среднему качеству прочтений (в процентах)
    :return: список словарей отфильтрованный по среднему качеству прочтений
    """
    filtered = []
    for d in dicts:
        qualities = [ord(i) - 33 for i in d['quality']]
        mean = sum(qualities) / len(qualities)
        if mean >= qual_threshold:
            filtered.append(d)
    return filtered


def failed_filter(full_dicts, filtered_dicts):
    """
    Создание списка словарей с непрошедшими фильтрацию прочтениями

    :param full_dicts: список словарей полученный из функции making_dicts (все прочтения без фильтрации)
    :param filtered_dicts: список словарей прошедший фильтрацию
    :return: список словарей с прочтениями непрошедшими фильтрацию
    """
    failed_dicts = []
    for i in full_dicts:
        if i not in filtered_dicts:
            failed_dicts.append(i)
    return failed_dicts


def file_writing_passed(filtered_dicts, prefix):
    """
    Создание файлов с прочтениями прошедшими фильтрацию.
    Название {prefix}_passed.fastq.

    :param filtered_dicts: список словарей с прочтениями прошедшими фильтраци
    :param prefix: префикс в начале названия файла
    :return: None
    """
    with open(f'{prefix}_passed.fastq', 'w') as f:
        for i in filtered_dicts:
            for j in i.values():
                print(j, file=f)


def file_writing_failed(failed_dicts, prefix):
    """
    Создание файлов с прочтениями не прошедшими фильтрацию.
    Название {prefix}_failed.fastq
    (запись происходит только при значении параметра save_filtered=True)

    :param failed_dicts: список словарей с прочтениями не прошедшими фильтрацию
    :param prefix: префикс в начале названия файла
    :return None
    """
    with open(f'{prefix}_failed.fastq', 'w') as f:
        for i in failed_dicts:
            for j in i.values():
                print(j, file=f)


def main(input_fastq, output_file_prefix, gc_bounds=(0, 100),
         length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=False):
    """
    Функция, в которой происходит вся фильтрация и запись файлов.

    :param input_fastq: файл .fastq, который надо отфильтровать
    :param output_file_prefix: префикс, с которым будут создаваться новые файлы
    с прошедшими и непрошедшими фильтрацию прочтениями
    :param gc_bounds: границы фильтрации по GC-составу (в процентах)
    :param length_bounds: границы фильтрации по длине (в нуклеотидах)
    :param quality_threshold: нижняя граница фильтрации по среднему качеству прочтений (в процентах)
    :param save_filtered: параметр, указывающий нужно ли сохранять отдельным файлом прочтения не прошедшие фильтрацию
    :return: None
    """

    with open(input_fastq) as file:
        full_dicts = making_dict(file)  # список словарей с 4 элементами соответсвуюшим строчкам одного прочтения

        # фильтрация по длине прочтений
        len_filtered_dicts = filter_len(full_dicts, length_bounds)

        # фильтрация по количеству GC
        gc_filtered_dicts = filter_gc_percentage(len_filtered_dicts, gc_bounds)

        # фильтрация по качеству прочтений
        final_filtered_dicts = filter_mean_quality(gc_filtered_dicts, quality_threshold)

        # список словарей с прочтениями непрошедшими фильтрацию
        failed_dicts = failed_filter(full_dicts, final_filtered_dicts)

        # запись файлов
        file_writing_passed(final_filtered_dicts, output_file_prefix)

        if save_filtered:
            file_writing_failed(failed_dicts, output_file_prefix)
