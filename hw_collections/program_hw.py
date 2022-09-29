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


def seq_inp_check(sequence):
    """
    Функция, проверяющая корректность введенной последовательности
    нуклеотидов: чтобы это были именно нуклеотиды и в одной
    последовательности не было тимина и урацила.
    В зависимости от результата возвращает строчку, которую
    обработает функция execution

    :param sequence: последовательность нуклеотидов
    :return: строка, которую далее принимает функция execution
    """
    for i in sequence:
        if i.lower() not in ['a', 'c', 't', 'g', 'u']:
            return 'wrong alph'
    if sequence.lower().find('t') != -1 and sequence.lower().find('u') != -1:
        return 'rna and dna'
    else:
        return 'ok'


def execution(cmd):
    """
    Функция принимает команду, которую хочет исполнить пользователь.
    Просит ввести последовательность и в случае успешной проверки
    последовательности нуклеотидов функцией seq_inp_check
    исполняет функции transcribe, reverse, complement и reverse_complement.
    При неверном вводе последовательности выводит соообщение
    об ошибке и просит ввести заново последовательность.

    :param cmd: команда, которую хочет исполнить пользователь
    :return: результат исполнения команды или сообщение об ошибке
    """
    while True:
        seq = input('Enter sequence: ')
        if seq_inp_check(seq) == 'ok':
            print(cmd(seq))
            break
        elif seq_inp_check(seq) == 'wrong alph':
            print("Invalid Alphabet! Try Again.")
        elif seq_inp_check(seq) == 'rna and dna':
            print("There are T and U in your sequence.")


def transcribe(sequence):
    """
    Функция, транскрибирубщая последовательность ДНК.
    Если была введена последовательнсоть РНК, то просит ввести
    последовательность заново.

    :param sequence: последовательность нуклеотидов
    :return: транскрибированную последовательность ДНК или
    сообщение об ошибке
    """
    newseq = ''
    while True:
        if sequence.lower().find('u') != -1:
            print("I can't transcribe RNA sequence. Try Again!")
            sequence = input('Enter sequence: ')
            continue
        else:
            for i in sequence:
                newseq += d_transcription[i]
            break
    return newseq


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
