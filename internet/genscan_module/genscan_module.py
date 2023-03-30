import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from dataclasses import dataclass, field


class BadResponse(Exception):
    pass


@dataclass
class GenscanOutput:
    status: int
    cds_list: list = field(default_factory=lambda: [])
    intron_list: pd.DataFrame = pd.DataFrame()
    exon_list: pd.DataFrame = pd.DataFrame()


def run_genscan(sequence=None, sequence_file=None,
                organism="Vertebrate", exon_cutoff=1.00,
                sequence_name=""):
    if sequence_file:
        file = open(sequence_file, 'rb')
    else:
        file = sequence_file

    response = requests.post('http://hollywood.mit.edu/cgi-bin/genscanw_py.cgi',
                             data={'-s': sequence,
                                   '-o': organism,
                                   '-e': exon_cutoff,
                                   '-n': sequence_name,
                                   '-p': 'Predicted peptides only'},
                             files={'-u': file})

    if sequence_file:
        file.close()

    if response.status_code % 100 == 4:
        raise BadResponse(f'You recieved response with {response.status_code} status code')

    soup = BeautifulSoup(response.content, "lxml")
    output_full = soup.find('pre').text

    protein_re = re.findall(pattern=r'^>.+\n{2}([A-Z\n]+)', string=output_full, flags=re.MULTILINE)

    if not protein_re:
        print('Predicted protein was not found')
        return GenscanOutput(response.status_code)

    cds_list = list(map(lambda x: x.strip().replace('\n', ''), protein_re))

    exon_re_full_table = re.search(pattern=r'Predicted genes/exons:[\n\w\./ \-+]+', string=output_full)
    exon_re_list = re.findall(pattern=r' \d[\w\. +-]+', string=exon_re_full_table.group(0))

    exon_list = list(map(lambda x: re.split(r' +', x.strip())[:5],
                         filter(lambda x: 'PlyA' not in x, exon_re_list)))
    exon_df = pd.DataFrame(exon_list, columns=['Number', 'Type', 'Strand', 'Start', 'End']). \
        astype({'Start': 'int64', 'End': 'int64'})

    intron_df = pd.DataFrame(columns=['Number', 'Strand', 'Start', 'End'])

    if exon_df.shape[0] > 1:
        for i in range(exon_df.shape[0] - 1):
            intron_df.loc[i] = exon_df.loc[i, exon_df.columns != 'Type']
            intron_df.loc[i, 'Start'] = exon_df.loc[i, 'End'] + 1
            intron_df.loc[i, 'End'] = exon_df.loc[i + 1, 'Start'] - 1

    return GenscanOutput(response.status_code, cds_list, intron_df, exon_df)


if __name__ == '__main__':

    ges_res_1 = run_genscan('''AATCTCAACTATGAAGCTCTTGCCGTTGATTCCTCTTGTCGCGTCTACCGCAATTCCAGACTCTGGTGTA
    TCCACTGGCACCAAAGACCTGTAAGATACTTCTTTTTCGGACGACCCGAACTTCCCTTAGAACCATCTAG
    TTTTGCTTACCATGCACCAGCTCTAAACGAGACGAACCATACATATTTGATGTCACGTTTCGAGTTGGTC
    CAGCCGGGGCTAACGTCGCGCCATTCTCTGGATCTGTGTACGTCCAGGATGGTATTACCCCACTTGTTCG
    TTCAGGTTCAGGATCTTCGGTCTCGGGTCGCAGTTACAACGCTTTCAGAGGAATAGTGTACTTCACATTT
    GCTCAAGGCTTCAACCAGTACTCCGCATCGACTCGATTTGGTGTCTACCCTGATACTGGATTAATTGTCG
    ACTCGGACGGCAGACTAATCTACGGGACCGCGCCCCGGAAAGCCTGCATCGACTATTCACCTCATGGTCC
    CACCGACGTTTGTTCTGTAACAATTACCAGGTCTTAGTAGGAATAGTTGAAAAGACCTTACTACCATCCC
    CCTCTTACCGAATTAATTGAAAAATTA''')

    ges_res_2 = run_genscan(sequence_file='../data/sequence.fasta')

    print(ges_res_1.exon_list)
    print(ges_res_2.intron_list)
