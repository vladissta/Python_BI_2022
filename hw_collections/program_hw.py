d_complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
                'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}

d_transcription = {'A': 'A', 'T': 'U', 'G': 'G', 'C': 'C',
                   'a': 'a', 't': 'u', 'g': 'g', 'c': 'c'}

commands = '''
exit — завершение исполнения программы
transcribe — напечатать транскрибированную последовательность
reverse — напечатать перевёрнутую последовательность
complement — напечатать комплементарную последовательность
reverse complement — напечатать обратную комплементарную последовательность
'''


def seq_inp_check(sequence):
    for i in sequence:
        if i.lower() not in ['a', 'c', 't', 'g', 'u']:
            return 'wrong alph'
    if sequence.lower().find('a') != -1 and sequence.lower().find('u') != -1:
        return 'rna and dna'
    else:
        return 'ok'


def execution(cmd):
    while True:
        seq = input('Enter sequence: ')
        if seq_inp_check(seq) == 'ok':
            print(cmd(seq))
            break
        elif seq_inp_check(seq) == 'wrong alph':
            print("Invalid Alphabet! Try Again.")
        elif seq_inp_check(seq) == 'rna and dna':
            print("There are T and U in your sequence.")


def reverse(sequence):
    return sequence[::-1]


def complement(sequence):
    newseq = ''
    for i in sequence:
        newseq += d_complement[i]
    return newseq


def reverse_complement(sequence):
    return reverse(complement(sequence))


def transcribe(sequence):
    newseq = ''
    for i in sequence:
        newseq += d_transcription[i]
    return newseq


print(f'List of commands: {commands}')

while True:

    command = input('Enter command: ')

    if command == 'exit':
        print('Good luck!')
        break

    elif command == 'transcribe':
        execution(transcribe)

    elif command == 'reverse':
        execution(reverse)

    elif command == 'complement':
        execution(complement)

    elif command == 'reverse complement':
        execution(reverse_complement)

    else:
        print('''\nTry to print command correctly!
        
List of commands: ''',
              commands)
