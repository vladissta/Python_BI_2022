def making_list(file):
    """
    Создание из файла списка из строк этого файла для дальнейшего использования

    :param file: файл .fastq
    :return: список из строк файла
    """
    full_list = []
    for line in file:
        x = [line.strip()]
        for i in range(3):
            x.append(file.readline().strip())
        full_list.append(x)
    return full_list


def making_dicts(full_list):
    """
    Создание списка словарей с 4 элементами соответсвуюшим строчкам одного прочтения

    :param full_list: список из строк файла полученный из функции making_list
    :return: список из словарей
    """
    d = []
    for i in full_list:
        d.append({'name': i[0], 'seq': i[1], 'plus': i[2], 'quality': i[3]})
    return d


def filter_len(dicts, length_bounds):
    """
    Создание списка словарей прочтений прошедших фильтрацию по длине прочтений.
    Дается две границы длины, выбираются прочтения длиной попадающие в эти границы включительно

    :param dicts: список словарей полученный из функции full_dicts
    :param length_bounds: границы фильтрации по длине (в нуклеотидах)
    :return: список словарей прошедший фильтрацию по длине прочтений
    """
    filtered = []
    for i in dicts:
        if length_bounds[0] <= len(i['seq']) <= length_bounds[1]:
            filtered.append(i)
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
    for i in dicts:
        c = 0
        for j in i['seq']:
            if j.upper() in ["G", "C"]:
                c += 1
        prc = (c / len(i['seq'])) * 100
        if len(gc_bounds) == 2:
            if gc_bounds[0] <= prc <= gc_bounds[1]:
                filtered.append(i)
        else:
            if prc <= gc_bounds:
                filtered.append(i)
    return filtered


def filter_mean_quality(dicts, qual_threshold):
    """
    Создание списка словарей прочтений прошедших фильтрацию по среднему качеству прочтений.
    Дается одна граница, выбираются прочтения по среднему качеству большие и равные границе

    :param dicts: список словарей полученный из функции filter_gc_percentage
    :param qual_threshold: граница фильтрации по среднему качеству прочтений (в процентах)
    :return: список словарей отфильтрованный по среднему качеству прочтений
    """
    filtered = []
    for i in dicts:
        s = 0
        for j in i['quality']:
            s += ord(j)
        mean = s / len(i['quality'])
        if mean >= qual_threshold:
            filtered.append(i)
    return filtered


def failed_filter(full_dicts, filtered_dicts):
    """
    Создание списка словарей с непрошедшими фильтрацию прочтениями

    :param dicts: список словарей полученный из функции making_dicts (все прочтения без фильтрации)
    :param filtered_dicts: список словарей прошедший фильтрацию
    :return: список словарей с прочтениями непрошедшими фильтрацию
    """
    failed_dicts = []
    for i in full_dicts:
        if i not in filtered_dicts:
            failed_dicts.append(i)
    return failed_dicts


def file_writing(filtered_dicts, failed_dicts, save_filtered, prefix):
    """
    Создание файлов с прочтениями прошедшими фильтрацию. Название {prefix}_passed.fastq.
    Создание файлов с прочтениями не прошедшими фильтрацию. Название {prefix}_failed.fastq (запись происходит только
    при значении параметра save_filtered=True)

    :param filtered_dicts: список словарей с прочтениями прошедшими фильтрацию
    :param failed_dicts: список словарей с прочтениями не прошедшими фильтрацию
    :param save_filtered: параметр, указывающий нужно ли сохранять отдельным файлом прочтения не прошедшие фильтрацию
    :param prefix: префикс в начале названия файла
    :return: None
    """
    with open(f'{prefix}_passed.fastq', 'w') as f:
        for i in filtered_dicts:
            for j in i.values():
                print(j, file=f)

    if save_filtered:
        with open(f'{prefix}_failed.fastq', 'w') as f:
            for i in failed_dicts:
                for j in i.values():
                    print(j, file=f)


def main(input_fastq, output_file_prefix, gc_bounds=(0, 100),
         length_bounds=(0, 2 ** 32), quality_threshold=0, save_filtered=True):
    """
    Функция, в которой происходит вся фильтрация и запись файлов.

    :param input_fastq: файл .fastq, который надо отфильтровать
    :param output_file_prefix: префикс, с которым будут создаваться новые файлы
    с прошедшими и непрошедшими фильтрацию прочтениями
    :param gc_bounds: границы фильтрации по GC-составу (в процентах)
    :param length_bounds:   границы фильтрации по длине (в нуклеотидах)
    :param quality_threshold: нижняя граница фильтрации по среднему качеству прочтений (в процентах)
    :param save_filtered: параметр, указывающий нужно ли сохранять отдельным файлом прочтения не прошедшие фильтрацию
    :return: None
    """

    with open(input_fastq) as file:
        full_list = making_list(file)  # создание из fastq файла списка для использования далее
        full_dicts = making_dicts(full_list)  # список словарей с 4 элементами соответсвуюшим строчкам одного прочтения

        # фильтрация по длине прочтений
        len_filtered_dicts = filter_len(full_dicts, length_bounds)

        # фильтрация по количеству GC
        gc_filtered_dicts = filter_gc_percentage(len_filtered_dicts, gc_bounds)

        # фильтрация по качеству прочтений
        final_filtered_dicts = filter_mean_quality(gc_filtered_dicts, quality_threshold)

        # список словарей с прочтениями непрошедшими фильтрацию
        failed_dicts = failed_filter(full_dicts, final_filtered_dicts)

        # запись файлов
        file_writing(final_filtered_dicts, failed_dicts, save_filtered, output_file_prefix)
