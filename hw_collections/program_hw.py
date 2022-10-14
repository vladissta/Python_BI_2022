# Словарь с комплиментраными нуклеотидами для ДНК
d_complement_dna = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
                    'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}

# Словарь с комплиментраными нуклеотидами для РНК
d_complement_rna = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G',
                    'a': 'u', 'u': 'a', 'g': 'c', 'c': 'g'}

# Словарь для транскрипции (А превращает в Т)
d_transcription = {'A': 'A', 'T': 'U', 'G': 'G', 'C': 'C',
                   'a': 'a', 't': 'u', 'g': 'g', 'c': 'c'}
# Список команд
commands = '''
exit — завершение исполнения программы
transcribe — напечатать транскрибированную последовательность
reverse — напечатать перевёрнутую последовательность
complement — напечатать комплементарную последовательность
reverse complement — напечатать обратную комплементарную последовательность
'''


def rna_dna_check(sequence):
    """
    Функция, проверяющая корректность введенной последовательности
    нуклеотидов: чтобы в последовательности не было тимина и урацила

    :param sequence: последовательность нуклеотидов
    :return: True/False
    """
    if {'u', 't'}.issubset(set(sequence.lower())):
        return False
    return True


def alphabet_check(sequence):
    """
    Функция, проверяющая корректность введенной последовательности
    нуклеотидов: чтобы это были именно нуклеотиды

    :param sequence: последовательность нуклеотидов
    :return: True/False
    """
    if not set(sequence.lower()).issubset({'a', 'c', 't', 'g', 'u'}):
        return False
    return True


def dna_check(sequence):
    """
    Проверяет является ли послдеовательность нуклеотидов РНК, если нет, то выводит сообщение об ошибке и просит ввести
    последовательность снова

    :param sequence: последовательность нуклеотидов
    :return: Проверенная последовательность ДНК для трансляции
    """
    seq = sequence
    while True:
        if 'u' in set(seq.lower()):
            print('I cannot transcribe RNA sequence')
            seq = input('Enter sequence: ')
        else:
            return seq


def execution(cmd):
    """
    Функция принимает команду, которую хочет исполнить пользователь.
    Просит ввести последовательность и в случае успешной проверки
    последовательности нуклеотидов функциями rna_dna_check и alphabet_check
    исполняет функции transcribe, reverse, complement и reverse_complement (в зависимости от выбора пользователя).
    При неверном вводе последовательности выводит соообщение об ошибке и просит ввести заново последовательность.
    При вводе последовательности с урацилом и тимином выводит соообщение об ошибке
    и просит ввести заново последовательность.

    :param cmd: команда, которую хочет исполнить пользователь
    :return: результат исполнения команды или сообщение об ошибке
    """
    while True:
        seq = input('Enter sequence: ')
        if not alphabet_check(seq):
            print("Invalid Alphabet! Try Again.")
        elif not rna_dna_check(seq):
            print("There are T and U in your sequence.")
        else:
            print(cmd(seq))
            break


def transcribe(sequence):
    """
    Функция, транскрибирубщая последовательность ДНКБ проверенную функцией dna_check

    :param sequence: последовательность нуклеотидов
    :return: транскрибированную последовательность ДНК
    """
    return ''.join([d_transcription[nucl] for nucl in dna_check(sequence)])


def reverse(sequence):
    """
    Возвращает перевёрнутую последовательность

    :param sequence: последовательность нуклеотидов
    :return: перевёрнутная последовательность нуклеотидов
    """
    return sequence[::-1]


def complement(sequence):
    """
    Взависимости от того, была введена последовательность ДНК или РНК,
    возвращает комплементарную последоваетльность

    :param sequence: последовательность нуклеотидов
    :return: комплементарная последовательность нуклеотидов
    """
    newseq = ''
    if sequence.lower().find('t') != -1:
        for i in sequence:
            newseq += d_complement_dna[i]
    else:
        for i in sequence:
            newseq += d_complement_rna[i]
    return newseq


def reverse_complement(sequence):
    """
    Взависимости от того, была введена последовательность ДНК или РНК,
    возвращает комплементарную и повернутую последоваетльность

    :param sequence: последовательность нуклеотидов
    :return: комплементарная и перевернутая последовательность нуклеотидов

    :param sequence:
    :return:
    """
    return reverse(complement(sequence))


# Выводит в начале список команд для пользователя
print(f'List of commands: {commands}')

# Бесконечный цикл, из которого выйти можно только
# при наборе команды exit
while True:

    # Просит ввести команду
    command = input('Enter command: ')

    # Если команда exit, то заканчивает команду
    if command == 'exit':
        print('Good luck!')
        break

    # При вводе команд происходит проверка последовательности
    # и исполение команды при корректном вводе последовательности
    elif command == 'transcribe':
        execution(transcribe)

    elif command == 'reverse':
        execution(reverse)

    elif command == 'complement':
        execution(complement)

    elif command == 'reverse complement':
        execution(reverse_complement)

    # Если команда введена некорректно, то просит ввести ее еще раз
    else:
        print('''\nTry to print command correctly!\n\nList of commands: ''', commands)
